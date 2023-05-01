import json
from redis import Redis
from datetime import datetime

class Analyst:

    def __init__(self, platform):
        self.platform = platform

    def dump_new_scopes(self, output='./analysis') -> None:
        with open(self.platform.get_path(), 'r') as file:
            programs = list(map(lambda prog: {'id': prog.get(self.platform.get_program_id(prog)),
                                              'name': self.platform.get_program_name(prog),
                                              'last_updated': self.platform.get_program_last_updated(prog),
                                              'domains': self.platform.get_program_domains(prog)}, 
                                               json.load(file)))
            client = Redis()
            updates = {}
            for prog in programs:
                _key = f'{self.platform.get_name()}:{prog["id"]}'
                is_updated = client.sadd(f'{_key}:last_updated', 
                                         prog['last_updated'].timestamp())
                if is_updated:
                    new_scopes = [ domain
                        for domain in prog['domains']
                        if client.sadd(f'{_key}:domains', domain)
                    ]

                    updates[prog['name']] = {
                        'last_update': prog['last_updated'].strftime('%Y-%m-%d %H:%M:%S'),
                        'new_scopes': new_scopes
                    }
            
            with open(f'{output}/{self.platform.name}.json', 'w') as writer:
                json.dump(updates, writer)