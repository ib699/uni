import rabbitMQ
import object_storage
import shazam
import spotify
import postgresql


def handle_error(song_id):
    postgresql_ins.update_client_state(song_id, "Failure")


def handle_queue(song_id):
    try:
        file_name = song_id + ".wav"
        object_storage.download(file_name)
        song_name = shazam.getSongName(file_name)
        spotify_id = spotify.get_song_id(song_name)
        postgresql_ins.update_client_song_id(song_id, spotify_id)
        postgresql_ins.update_client_state(song_id, "Ready")
        print("done")
    except Exception as e:
        postgresql_ins.update_client_state(song_id, "failure")


if __name__ == "__main__":
    print("Rabbit listener started")
    postgresql_ins = postgresql.Postgresql()
    rabbitMQ_obj = rabbitMQ.RabbitMQ()
    rabbitMQ_obj.start_listening(handle_queue)
    # handle_queue("21")
