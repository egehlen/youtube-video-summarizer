from langchain.schema.runnable import Runnable
from rich.box import SIMPLE
from ..common import VideoDescriptor, global_console
from rich.table import Table
from rich.panel import Panel

class DisplayOutputRunnable(Runnable):

    def invoke(self, input: VideoDescriptor, *args) -> VideoDescriptor:
        self.display_output(input)
        return input

    def display_output(self, descriptor: VideoDescriptor) -> None:
        title_panel = self.get_title_panel(descriptor)
        header_table = self.get_header_table(descriptor)
        content_table = self.get_content_table(descriptor)
        highlights_table = self.get_highlights_table(descriptor)
        steps_table = self.get_steps_table(descriptor)

        global_console.print("\n")
        global_console.print(title_panel)
        global_console.print(header_table)
        global_console.print(content_table)
        global_console.print(highlights_table)
        global_console.print(steps_table)

    @staticmethod
    def get_title_panel(descriptor: VideoDescriptor) -> Panel:
        return Panel(f"Video: {descriptor.title}", title_align="left", style="bold yellow")

    @staticmethod
    def get_header_table(descriptor: VideoDescriptor) -> Table:
        grid = Table(box=SIMPLE, show_header=False)
        grid.add_column(justify="right", min_width=3)
        grid.add_column(min_width=1)
        grid.add_column(justify="left")
        grid.add_row("Title :", "", descriptor.title)
        grid.add_row("URL :", "", descriptor.url)
        grid.add_row("Channel :", "", descriptor.channel)
        grid.add_row("Video length :", "", descriptor.duration)
        grid.add_row("Categories :", "", "".join(descriptor.categories))
        grid.add_row("Target Language: ", "", descriptor.target_language)
        return grid

    @staticmethod
    def get_content_table(descriptor: VideoDescriptor) -> Table:
        table = Table(box=SIMPLE)

        table.add_column("Summary", justify="left", style="cyan")
        table.add_row(descriptor.summary)

        return table

    @staticmethod
    def get_highlights_table(descriptor: VideoDescriptor) -> Table:
        if not descriptor.highlights:
            return Table()

        table = Table(box=SIMPLE)
        table.add_column("Highlights", justify="left", style="green")
        for highlight in descriptor.highlights: table.add_row(f" - {highlight}")
        return table

    @staticmethod
    def get_steps_table(descriptor: VideoDescriptor) -> Table:
        if not descriptor.steps:
            return Table()

        table = Table(box=SIMPLE)
        table.add_column("Steps", justify="left", style="green")
        for i, step in enumerate(descriptor.steps): table.add_row(f" {(i+1)}. {step}")
        return table