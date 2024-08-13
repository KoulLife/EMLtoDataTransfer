import os

from select_folder import select_folder
from send import send
from separate_dat import check_eml_in_folder


def send_gateway(server_entry,
                 port_entry,
                 sender_entry,
                 receiver_entry,
                 delay_entry,
                 retries_entry,
                 eml_location,
                 count_label,
                 status_label):
    location = os.path.dirname(check_eml_in_folder(eml_location))
    print(location)
    print(type(location))
    send(server_entry, port_entry, sender_entry, receiver_entry, delay_entry, retries_entry, location, count_label, status_label)
