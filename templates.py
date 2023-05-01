class BaseTemplate:
    def __init__(self, path, 
                 name, program_id,
                 program_name, program_last_updated, 
                 program_domains, program_domains_endpoint) -> None:
        self.path = path
        self.name = name
        self.program_id = program_id
        self.program_name = program_name
        self.program_last_updated = program_last_updated
        self.program_domains = program_domains
        self.program_domains_endpoint = program_domains_endpoint

class IntigritiTemplate(BaseTemplate):
    def __init__(self) -> None:
        super().__init__(path='./programs/intigriti.json', 
                         name='intigriti',
                         program_id='programId',
                         program_name='name',
                         program_last_updated='lastUpdatedAt',
                         program_domains='domains',
                         program_domains_endpoint='endpoint')