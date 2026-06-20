import rumps
import subprocess

def get_now_playing():
    # Apple Music Now Playing
    apple_script_music = '''
    tell application "System Events"
        if (name of processes) contains "Music" then
            tell application "Music"
                if player state is playing then
                    return name of current track & " - " & artist of current track
                end if
            end tell
        end if
    end tell
    return ""
    '''
    # Spotify Now Playing

    apple_script_spotify = '''
    tell application "System Events"
        if (name of processes) contains "Spotify" then
            tell application "Spotify"
                if player state is playing then
                    return name of current track & " - " & artist of current track
                end if
            end tell
        end if
    end tell
    return ""
    '''

    for script in [apple_script_music, apple_script_spotify]:
        result = subprocess.run(
            ['osascript', '-e', script],
            capture_output=True, text=True
        )
        track = result.stdout.strip()
        if track:
            return track
        
    return None


class NowPlayingApp(rumps.App):
    def __init__(self):
        super().__init__("♫", quit_button="Quit")
        self.update_timer = rumps.Timer(self.update_status, 5)
        self.update_timer.start()

    @rumps.timer(5)
    def update_status(self, _):
        track = get_now_playing()
        if track:
            display = track if len(track) <= 40 else track [:37] + "..."
            self.title = f"Now Playing: {display}"
        else:
            self.title = "♫"

if __name__ == "__main__":
    NowPlayingApp().run()