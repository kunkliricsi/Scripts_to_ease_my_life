#include <stdio.h>
    #include <stdlib.h>
    #include <sys/types.h>
    #include <unistd.h>

    int main()
    {
        setuid(0);
        system("/usr/local/bin/adaptive-brightness/adaptive-brightness-enabler.sh");
        return 0;
    }