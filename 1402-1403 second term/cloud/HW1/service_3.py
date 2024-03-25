import postgresql
import spotify
import mail


def make_email_string(data):
    string = "Hello your recommended top 10 list is:\n"
    for name in data:
        string = " <(--)>  ".join([string, name])
    return string


def handle_ready(lists):
    print(lists)
    for item in lists:
        id = item[0]
        email_address = item[1]
        spotify_id = item[3]
        try:
            data = spotify.get_recommended(spotify_id)
            send_string = make_email_string(data)
            mail.send_mail(email_address, send_string)
            postgresql_ins.update_client_state(id, "Done")
        except Exception as e:
            postgresql_ins.update_client_state(id, "failure")


def loop_check():
    while True:
        lists = postgresql_ins.get_clients_ready()
        if lists != None:
            handle_ready(lists)
        continue


if __name__ == "__main__":
    print("Status listener started")
    postgresql_ins = postgresql.Postgresql()
    loop_check()
