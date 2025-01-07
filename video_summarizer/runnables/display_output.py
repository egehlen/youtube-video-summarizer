from langchain.schema.runnable import Runnable
from rich.box import SIMPLE
from ..common import VideoDescriptor, global_console
from rich.table import Table

class DisplayOutputRunnable(Runnable):

    def invoke(self, input: VideoDescriptor, *args) -> None:
        self.display_output(input)

    def display_output(self, descriptor: VideoDescriptor) -> None:
        header_table = self.get_header_table(descriptor)
        content_table = self.get_content_table(descriptor)

        global_console.print("\n")
        global_console.print(header_table)
        global_console.print(content_table)
        global_console.print(descriptor.highlights)
        global_console.print(descriptor.steps)

    @staticmethod
    def get_header_table(descriptor: VideoDescriptor) -> Table:
        grid = Table(box=SIMPLE, title=f"# Video: {descriptor.title}", title_justify="left", title_style="bold yellow")
        grid.add_column(justify="right", min_width=3)
        grid.add_column(min_width=1)
        grid.add_column(justify="left")
        grid.add_row("Title :", "", descriptor.title)
        grid.add_row("URL :", "", descriptor.url)
        grid.add_row("Channel :", "", descriptor.channel)
        return grid

    @staticmethod
    def get_content_table(descriptor: VideoDescriptor) -> Table:
        table = Table(box=SIMPLE)

        table.add_column("Summary", justify="left", style="cyan")
        table.add_row(descriptor.summary)

        return table