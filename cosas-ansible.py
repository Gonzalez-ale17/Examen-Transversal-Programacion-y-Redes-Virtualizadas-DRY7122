#COMANDOS DE .YAML# ##ipv6-loopback,respaldo-show,apache-local#

---
- name: ipv6 en la loopback33
  hosts: CSR1kv
  gather_facts: false
  connection: network_cli

  tasks:
    - name: configuracion de loopback33
      ios_config:
        lines:
          - interface Loopback33
          - ipv6 address 3001:ABCD:ABCD:1::1/128
          - ipv6 address FE80::1 link-local

#############################


---
- name: respaldo del show running
  hosts: CSR1kv
  gather_facts: false
  connection: network_cli

  tasks:
    - name: realiza "show running-config"
      ios_command:
        commands:
          - show running-config
      register: salida

    - name: guarda el archivo
      copy:
        content: "{{ salida.stdout[0] }}"
        dest: "./show_run_{{ inventory_hostname }}.txt"

#############################

---
- name: apache en puerto 9999
  hosts: localhost
  become: yes

  tasks:
    - name: instalar Apache
      apt:
        name: apache2
        state: present
        update_cache: yes

    - name: detener Apache antes de reconfigurar
      service:
        name: apache2
        state: stopped

    - name: cambiar puerto en ports.conf
      lineinfile:
        path: /etc/apache2/ports.conf
        regexp: '^Listen '
        line: 'Listen 9999'

    - name: cambiar el virtual host a puerto 9999
      replace:
        path: /etc/apache2/sites-available/000-default.conf
        regexp: '^<VirtualHost \*:.*>'
        replace: '<VirtualHost *:9999>'

    - name: Iniciar Apache
      service:
        name: apache2
        state: started

