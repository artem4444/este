def port_check():
    import psutil

    port = 8501
    for conn in psutil.net_connections(kind='inet'):
        if conn.laddr.port == port:
            print(f"Port {port} is being used by PID {conn.pid}")

        else:
            print(f"Port {port} is not being used")


if __name__ == '__main__':
    port_check()
