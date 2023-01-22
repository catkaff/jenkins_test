#!/bin/env python3
# -*- coding: utf-8 -*-
import json, sys, argparse, logging

def write_config(file_json_conf: str, sudo_obj: dict):
  try:
    with open(file_json_conf, 'w', encoding= 'utf-8') as fp:
      json.dump(sudo_obj, fp, ensure_ascii= False)
  except OSError as e:
    logging.error(f"Failed to open file \"{fp}\", caused by: ({e.errno}) {e.strerror}")
  else:
    with open(file_json_conf, "r", encoding='utf8') as file:
      config_json = json.load(file)
      logging.info(json.dumps(config_json, sort_keys=True, ensure_ascii=False, indent=4))
      return 0


def create_dict_from_parameters(search_base: str, sudo_rule_name: str, user: str, runasuser: str, runasgroup: str, host: str, commands: str,
                                netgroup_search_base: str, netgroup_name: str, netgroup_triple: list):
    sudo_obj = {}
    su_ob = {}
    su_ob['search_base'] = f'OU={search_base},OU=Information_systems,OU=Sudo_rules,OU=Services,OU=Linux_Services_Groups,OU=Дотсуп к ресурсам,OU=Группы,DC=homecredit,DC=ru'
    su_ob['sudo_rule_name'] = sudo_rule_name
    su_ob['user'] = user
    su_ob['command'] = ['/' + i for i in (' ' + commands).split(' /')[1:]]
    su_ob['runasuser'] = runasuser
    su_ob['runasgroup'] = runasgroup
    su_ob['order'] = "4"
    su_ob['option'] = ["!authenticate"]
    su_ob['host'] = host

    sudo_net = {}
    sudo_net['netgroup_search_base'] = netgroup_search_base
    sudo_net['netgroup_name'] = netgroup_name
    sudo_net['netgroup_triple'] = netgroup_triple
    if netgroup_search_base == '':
        sudo_net = {}
    else:
        sudo_obj['netgroup_object'] = sudo_net
    sudo_obj['sudo_object'] = su_ob
    return sudo_obj


if __name__ == '__main__':
# Настраиваем логгирование всех действий скрипта в файл
    logging.basicConfig(filename='create_json_sudo.log',
                        level=logging.DEBUG,
                        format='%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S', encoding='utf-8')


# define a Handler which writes INFO messages or higher to the sys.stderr
# Здесь настройка вывода выхлопа информационных сообщений скрипта еще и в консоль помимо записи лога файла
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    # add the handler to the root logger
    logging.getLogger('').addHandler(console)

    params = sys.argv
    separator = 'TT'
    separator_list = []

# Введу разделитель в сырую строку, для реализации считывания нетгрупп атрибутов
    for index_net, elem in enumerate(params):
        if elem == separator:
            separator_list.append(index_net)

    search_base = str(params[1])
    sudo_rule_name = str(params[2])
    user = str(params[3])
    runasuser = str(params[4])
    runasgroup = str(params[5])
    host = str(params[6])
    commands = ' '.join(params[7:separator_list[0]])
    file_json_conf = f'{sudo_rule_name}.json'

    print(f' LEN: {len(params)}  Separator: {separator_list[0]}')
    if (len(params)-1 > separator_list[0]) and (len(params)-1 - separator_list[0] >= 3):
        netgroup_search_base = f'OU={params[separator_list[0]+1]},OU=Information_systems,OU=Netgroups,OU=Services,OU=Linux_Services_Groups,OU=Дотсуп к ресурсам,OU=Группы,DC=homecredit,DC=ru'
        netgroup_name = str(params[separator_list[0]+2])
        netgroup_triple = params[separator_list[0]+3:]
        for i in range(len(netgroup_triple)):
            netgroup_triple[i] = f'({netgroup_triple[i]},  , homecredit.ru)'
    else:
        netgroup_search_base = ''
        netgroup_name = ''
        netgroup_triple = []

    sudo_obj = create_dict_from_parameters(search_base, sudo_rule_name, user, runasuser, runasgroup, host, commands, netgroup_search_base, netgroup_name, netgroup_triple)
    write_config(file_json_conf, sudo_obj)