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


def create_dict_from_parameters(search_base: str, sudo_rule_name: str, user: str, runasuser: str, runasgroup: str, host: str, commands: str):
    sudo_obj = {}
    su_ob = {}
    su_ob['search_base'] = search_base
    su_ob['sudo_rule_name'] = sudo_rule_name
    su_ob['user'] = user
    su_ob['command'] = ['/' + i for i in (' ' + commands).split(' /')[1:]]
    su_ob['runasuser'] = runasuser
    su_ob['runasgroup'] = runasgroup
    su_ob['order'] = "4"
    su_ob['option'] = ["!authenticate"]
    su_ob['host'] = host

    sudo_obj['netgroup_object'] = {}
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

    parser = argparse.ArgumentParser()
    parser.add_argument('--sbase', nargs='+', help='search_base')
    parser.add_argument('--srname', type=str, help='sudo_rule_name')
    parser.add_argument('--ug', type=str, help='user or %group for which this rule is used')

    parser.add_argument('--runasuser', type=str)
    parser.add_argument('--runasgroup', type=str)

    parser.add_argument('--suhost', type=str)
    parser.add_argument('--commands', nargs='+', help='commands for sudo')

    args = parser.parse_args()

    search_base = ' '.join(args.sbase)
    sudo_rule_name = args.srname
    user = args.ug
    runasuser = args.runasuser
    runasgroup = args.runasgroup
    host = args.suhost
    commands = ' '.join(args.commands)
    file_json_conf = f'{sudo_rule_name}.json'

    sudo_obj = create_dict_from_parameters(search_base, sudo_rule_name, user, runasuser, runasgroup, host, commands)
    write_config(file_json_conf, sudo_obj)