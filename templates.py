from datetime import datetime

class BaseTemplate:
    def __init__(self, path, 
                 name, program_id,
                 program_name, program_last_updated, 
                 program_domains) -> None:
        self.path = path
        self.name = name
        self.program_id = program_id
        self.program_name = program_name
        self.program_last_updated = program_last_updated
        self.program_domains = program_domains

    def nested_get(self, asset, attr):
        attr = getattr(self, attr).split('/')
        latest_asset = asset
        for key in attr:
            latest_asset = latest_asset.get(key)
        return latest_asset
    
    def get_path(self):
        return self.path

    def get_name(self):
        return self.name

    def get_program_id(self, asset):
        return asset.get(self.program_id)

    def get_program_name(self, asset):
        return asset.get(self.program_name)

    def get_program_last_updated(self, asset):
        return asset.get(self.program_last_updated)
    
    def get_program_domains(self, asset):
        return asset.get(self.program_domains)

class IntigritiTemplate(BaseTemplate):
    def __init__(self) -> None:
        super().__init__(path='./programs/intigriti.json', 
                         name='intigriti',
                         program_id='programId',
                         program_name='name',
                         program_last_updated='lastUpdatedAt',
                         program_domains='domains/endpoint')
    
    def get_program_last_updated(self, asset):
        return datetime.fromtimestamp(
                    asset.get(self.program_last_updated) 
                )
    
    def get_program_domains(self, asset):
        return list(map(lambda domain: domain['endpoint'], asset['domains'])) # Hardcoded
    

class HackeroneTemplate(BaseTemplate):
    def __init__(self) -> None:
        super().__init__(path='./programs/hackerone.json', 
                         name='hackerone',
                         program_id='id',
                         program_name='attributes/name',
                         program_last_updated='relationships/structured_scopes/data/attributes/updated_at',
                         program_domains='relationships/structured_scopes/data/attributes/asset_identifier')
    
    def get_program_name(self, asset):
        return self.nested_get(asset, 
                               'program_name')

    def get_program_last_updated(self, asset):
        try:
            data = asset.get('relationships').get('structured_scopes').get('data') # Hardcoded
            dates = list(map(lambda d: datetime.strptime(d.get('attributes').get('updated_at'), 
                                                        '%Y-%m-%dT%H:%M:%S.%fZ'), data))
            last_date = max(dates)
            return last_date 
        except:
            return 0
    
    def get_program_domains(self, asset):
        try:
            data = asset.get('relationships').get('structured_scopes').get('data') # Hardcoded
            domains = list(map(lambda d: d.get('attributes').get('asset_identifier'), data))

            return domains
        except:
            return []