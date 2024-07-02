#include <czmq.h>

int main(int argc, char **argv) {

     if (argc != 2) {
        printf("Usage: client port\n");
        return 1;
    }

    int port = atoi(argv[0]);

    zsock_t *requester = zsock_new(ZMQ_REQ);

    char addr[19];

    sprintf(addr, "tcp://localhost:%i", port);

    zsock_connect(requester, addr);

    zstr_send(requester, "hello, world");
    sleep(1);

    char *str = zstr_recv(requester);
    printf("%s\n", str);

    zsock_destroy(&requester);
}