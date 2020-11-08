from meters.MP730026 import MP730026


class OW18B(MP730026):
    """
    The Owon OW18B is very similar hardware to the Multicomp MP730026
    and since the library was originally written for the Multicomp
    we will just inherit that and use it.
    """

    def __init__(self, MAC: str = "autoscan", **kwargs):

        # Load the parent class values
        MP730026.__init__(self, MAC, **kwargs)

        # Local meter values below here.
        self.MAC = MAC
        self.output_to_console = False
        self.model = "Owon OW18B"
