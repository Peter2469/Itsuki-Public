import asyncio
import collections
import discord
from discord.ext import commands


EmojiSettings = collections.namedtuple('EmojiSettings', 'start back forward end close')

EMOJI_DEFAULT = EmojiSettings(
    start="\N{BLACK LEFT-POINTING DOUBLE TRIANGLE WITH VERTICAL BAR}",
    back="\N{BLACK LEFT-POINTING TRIANGLE}",
    forward="\N{BLACK RIGHT-POINTING TRIANGLE}",
    end="\N{BLACK RIGHT-POINTING DOUBLE TRIANGLE WITH VERTICAL BAR}",
    close="\N{BLACK SQUARE FOR STOP}"
)


class EmbedPaginator(commands.Paginator):
    def __init__(self, max_size=2048):
        super().__init__(prefix=None, suffix=None, max_size=max_size)

    def add_page(self, embed: discord.Embed):
        self._pages.append(embed)


class EmbedInterface:  # pylint: disable=too-many-instance-attributes
    """
    A message and reaction based interface for paginators.
    """

    def __init__(self, bot: commands.Bot, paginator: commands.Paginator, owner: discord.Member = None,
                 emojis: EmojiSettings = None):
        if not isinstance(paginator, commands.Paginator):
            raise TypeError('paginator must be a commands.Paginator instance')

        self._display_page = 0

        self.bot = bot

        self.message = None
        self.owner = owner
        self.paginator = paginator
        self.emojis = emojis or EMOJI_DEFAULT

        self.sent_page_reactions = False

        self.task: asyncio.Task = None
        self.update_lock: asyncio.Lock = asyncio.Semaphore(value=2)

    @property
    def pages(self):
        """
        Returns the paginator's pages without prematurely closing the active page.
        """
        # protected access has to be permitted here to not close the paginator's pages

        # pylint: disable=protected-access
        paginator_pages = list(self.paginator._pages)
        if len(self.paginator._current_page) > 1:
            paginator_pages.append('\n'.join(self.paginator._current_page) + '\n' + self.paginator.suffix)
        # pylint: enable=protected-access

        return paginator_pages

    @property
    def page_count(self):
        """
        Returns the page count of the internal paginator.
        """

        return len(self.pages)

    @property
    def display_page(self):
        """
        Returns the current page the paginator interface is on.
        """

        self._display_page = max(0, min(self.page_count - 1, self._display_page))
        return self._display_page

    @display_page.setter
    def display_page(self, value):
        """
        Sets the current page the paginator is on. Automatically pushes values inbounds.
        """

        self._display_page = max(0, min(self.page_count - 1, value))

    max_page_size = 2000

    @property
    def send_kwargs(self) -> dict:
        """
        A property that returns the kwargs forwarded to send/edit when updating the page.
        As this must be compatible with both `discord.TextChannel.send` and `discord.Message.edit`,
        it should be a dict containing 'content', 'embed' or both.
        """

        display_page = self.display_page
        page_num = f'\nPage {display_page + 1}/{self.page_count}'
        page = self.pages[display_page]
        if page.footer and page._footer['text'] != page_num:
            page._footer['text'] += " | " + page_num
        else:
            page.set_footer(text=page_num)
        return {'embed': page}

    async def add_line(self, *args, **kwargs):
        """
        A proxy function that allows this PaginatorInterface to remain locked to the last page
        if it is already on it.
        """

        display_page = self.display_page
        page_count = self.page_count

        self.paginator.add_line(*args, **kwargs)

        new_page_count = self.page_count

        if display_page + 1 == page_count:
            # To keep position fixed on the end, update position to new last page and update message.
            self._display_page = new_page_count
            self.bot.loop.create_task(self.update())

    async def send_to(self, destination: discord.abc.Messageable):
        """
        Sends a message to the given destination with this interface.
        This automatically creates the response task for you.
        """

        self.message = await destination.send(**self.send_kwargs)

        # add the close reaction
        await self.message.add_reaction(self.emojis.close)

        # if there is more than one page, and the reactions haven't been sent yet, send navigation emotes
        if not self.sent_page_reactions and self.page_count > 1:
            await self.send_all_reactions()

        if self.task:
            self.task.cancel()

        self.task = self.bot.loop.create_task(self.wait_loop())

    async def send_all_reactions(self):
        """
        Sends all reactions for this paginator, if any are missing.
        This method is generally for internal use only.
        """

        for emoji in self.emojis:
            if emoji:
                await self.message.add_reaction(emoji)
        self.sent_page_reactions = True

    @property
    def closed(self):
        """
        Is this interface closed?
        """

        if not self.task:
            return False
        return self.task.done()

    async def wait_loop(self):
        """
        Waits on a loop for reactions to the message. This should not be called manually - it is handled by `send_to`.
        """

        start, back, forward, end, close = self.emojis

        def check(payload: discord.RawReactionActionEvent):
            """
            Checks if this reaction is related to the paginator interface.
            """

            owner_check = not self.owner or payload.user_id == self.owner.id

            emoji = payload.emoji
            if isinstance(emoji, discord.PartialEmoji) and emoji.is_unicode_emoji():
                emoji = emoji.name

            return payload.message_id == self.message.id and \
                emoji and emoji in self.emojis and \
                payload.user_id != self.bot.user.id and owner_check

        try:
            while not self.bot.is_closed():
                payload = await self.bot.wait_for('raw_reaction_add', check=check, timeout=3600)

                emoji = payload.emoji
                if isinstance(emoji, discord.PartialEmoji) and emoji.is_unicode_emoji():
                    emoji = emoji.name

                if emoji == close:
                    await self.message.delete()
                    return

                if emoji == start:
                    self._display_page = 0
                elif emoji == end:
                    self._display_page = self.page_count - 1
                elif emoji == back:
                    self._display_page -= 1
                elif emoji == forward:
                    self._display_page += 1

                self.bot.loop.create_task(self.update())

                try:
                    await self.message.remove_reaction(payload.emoji, discord.Object(id=payload.user_id))
                except discord.Forbidden:
                    pass

        except asyncio.TimeoutError:
            await self.message.delete()

    async def update(self):
        """
        Updates this interface's messages with the latest data.
        """

        if self.update_lock.locked():
            return

        async with self.update_lock:
            if self.update_lock.locked():
                # if this engagement has caused the semaphore to exhaust,
                # we are overloaded and need to calm down.
                await asyncio.sleep(0.1)

            if not self.message:
                # too fast, stagger so this update gets through
                await asyncio.sleep(0.1)

            if not self.sent_page_reactions and self.page_count > 1:
                self.bot.loop.create_task(self.send_all_reactions())
                self.sent_page_reactions = True  # don't spawn any more tasks

            await self.message.edit(**self.send_kwargs)
