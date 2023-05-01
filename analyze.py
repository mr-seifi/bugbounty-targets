import json
from redis import Redis
from datetime import datetime

class Analyst:

    def __init__(self, platform):
        self.platform = platform

    def dump_new_scopes(self, output='./analysis') -> None:
        with open(self.platform.path, 'r') as file:
            programs = list(map(lambda prog: {'id': prog.get(self.platform.program_id),
                                              'name': prog.get(self.platform.program_name),
                                              'last_updated': prog.get(self.platform.program_last_updated),
                                              'domains': list(map(lambda domain: 
                                                                  domain[self.platform.program_domains_endpoint], 
                                                                  prog.get(self.platform.program_domains)))}, 
                                               json.load(file)))
            client = Redis()
            updates = {}
            for prog in programs:
                _key = f'{self.platform.name}:{prog["id"]}'
                is_updated = client.sadd(f'{_key}:last_updated', prog['last_updated'])
                if is_updated:
                    new_scopes = [ domain
                        for domain in prog['domains']
                        if client.sadd(f'{_key}:domains', domain)
                    ]

                    updates[prog['name']] = {
                        'last_update': datetime.fromtimestamp(prog['last_updated']).strftime('%Y-%m-%d %H:%M:%S'),
                        'new_scopes': new_scopes
                    }
            
            with open(f'{output}/{self.platform.name}.json', 'w') as writer:
                json.dump(updates, writer)