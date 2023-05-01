import json
from redis import Redis
from datetime import datetime

class Analyst:

    def dump_new_scopes(self, output='.') -> None:
        with open(self.platform.path, 'r') as file:
            programs = list(map(lambda prog: {'id': prog.get(self.program_id),
                                              'name': prog.get(self.program_name),
                                              'last_updated': prog.get(self.program_last_updated),
                                              'domains': list(map(lambda domain: 
                                                                  domain[self.program_domains_endpoint], 
                                                                  prog.get(self.program_domains)))}, 
                                               json.load(file)))
            client = Redis()
            updates = {}
            for prog in programs:
                _key = f'{self.name}:{prog["id"]}'
                is_updated = client.sadd(f'{_key}:last_updated', prog['last_updated'])
                if is_updated:
                    new_scopes = [ domain
                        for domain in prog['domains']
                        if client.sadd(f'{_key}:domains', domain) == 0
                    ]

                    updates[self._prog_name] = {
                        'last_update': datetime.fromtimestamp(prog['last_updated']).strftime('%Y-%m-%d %H:%M:%S'),
                        'new_scopes': new_scopes
                    }
            
            with open(f'{output}/{self.name}_analysis.json', 'w') as writer:
                json.dump(updates, writer)