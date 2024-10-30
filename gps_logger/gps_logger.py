import time
from threading import Thread, Lock
import subprocess

# Global variables for frequently used paths and parameters
UMOUNT_CMD = "/usr/bin/umount"
MOUNT_CMD = "/usr/bin/mount"
UUID = "6C6D-5FC1"
MOUNT_POINT = "/mnt/pendrive"
UID = "1000"  # User ID for `pi`
GID = "1000"  # Group ID for `pi`

# GPS data buffer and lock
gps_data_log = []
data_lock = Lock()

def is_pendrive_mounted():
    """Check if the pendrive is currently mounted."""
    result = subprocess.run([MOUNT_CMD], stdout=subprocess.PIPE, text=True)
    return MOUNT_POINT in result.stdout

def mount_usb():
    """Mount the pendrive using UUID if not already mounted."""
    if not is_pendrive_mounted():
        try:
            # Force unmount if mount point is in use
            subprocess.run([UMOUNT_CMD, MOUNT_POINT], check=False)
            # Mount using UUID with UID/GID options as integers
            subprocess.run([MOUNT_CMD, '-o', f'uid={UID},gid={GID}', f'UUID={UUID}', MOUNT_POINT], check=True)
            print("Pendrive mounted with options uid=1000,gid=1000.")
        except subprocess.CalledProcessError as e:
            print(f"Error mounting pendrive: {e}")

def remount_usb():
    """Force unmount and remount the pendrive if necessary."""
    subprocess.run([UMOUNT_CMD, MOUNT_POINT], check=False)
    time.sleep(1)  # Small delay to ensure unmount
    try:
        subprocess.run([MOUNT_CMD, '-o', f'uid={UID},gid={GID}', f'UUID={UUID}', MOUNT_POINT], check=True)
        print("Pendrive remounted successfully.")
    except subprocess.CalledProcessError:
        print("Error remounting pendrive.")

def unmount_usb():
    """Safely unmount the pendrive."""
    if is_pendrive_mounted():
        try:
            subprocess.run([UMOUNT_CMD, MOUNT_POINT], check=True)
            print("Pendrive unmounted.")
        except subprocess.CalledProcessError as e:
            print(f"Error unmounting pendrive: {e}")