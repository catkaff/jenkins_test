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


def create_dict_from_parameters(netgroup_search_base: str, netgroup_name: str, netgroup_triple: str):
    sudo_net = {}
    sudo_obj = {}

    sudo_net['netgroup_search_base'] = netgroup_search_base
    sudo_net['netgroup_name'] = netgroup_name
    sudo_net['netgroup_triple'] = netgroup_triple

    sudo_obj['netgroup_object'] = sudo_net
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

    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--infosystem', help='name of Information System', required=True)
    parser.add_argument('-n', '--netname', help='name of Information System', required=True)
    parser.add_argument('-t', '--net_triple', nargs='+', help='names of hosts aka os-0001 os-0002 ... os 000n', required=True)
    args = parser.parse_args()

    netgroup_search_base = f'OU={args.infosystem},OU=Information_systems,OU=Netgroups,OU=Services,OU=Linux_Services_Groups,OU=Дотсуп к ресурсам,OU=Группы,DC=homecredit,DC=ru'
    netgroup_name = args.netname
    netgroup_triple = ' '.join(args.net_triple)
    file_json_conf = f'{args.netname}.json'

    sudo_obj = create_dict_from_parameters(netgroup_search_base, netgroup_name, netgroup_triple)
    write_config(file_json_conf, sudo_obj)