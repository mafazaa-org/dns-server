#include <czmq.h>

int main(int argc, char** argv) {

    if (argc != 2) {
        printf("Usage: server port\n");
        return 1;
    }

    int port = atoi(argv[0]);

    zsock_t *responder = zsock_new(ZMQ_REP);
    char addr[11];
    sprintf(addr, "tcp://*:%i", port);
    int r = zsock_bind(responder, addr);

    if (r != port)
    {
        printf("Failed to bind to port\n");
        return 2;
    }

    while (true)
    {
        char *msg = zstr_recv(responder);
        if (!strcmp(msg, "hello, world")) {
            zstr_send(responder, "Gang");
        }

        free(msg);
    }

    zsock_destroy(&responder);
    free(addr);
}