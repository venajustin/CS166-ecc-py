#!/bin/bash

echo "Demo of two users Alice and Bob";
echo "Press Enter to continue through each step";

read nil;

echo "\$ python3 ../main.py getcurve secp192k1 ./domain";
read nil;
python3 ../main.py getcurve secp192k1 ./domain;

read nil;

ls -1R;

read nil;

echo "\$ cat domain";
cat domain;
echo -e "\n";
echo "\$ cat ./alice/private";
cat ./alice/private;
echo -e "\n";
echo "\$ cat ./bob/private";
cat ./bob/private;
echo -e "\n";

read nil;

echo "\$ python3 ../main.py genpublic ./domain ./alice/private ./alice/public";
read nil;
python3 ../main.py genpublic ./domain ./alice/private ./alice/public;

read nil;

echo "\$ python3 ../main.py genpublic ./domain ./bob/private ./bob/public";
read nil;
python3 ../main.py genpublic ./domain ./bob/private ./bob/public;


read nil;

echo "\$ cp ./alice/public ./bob/alice_pub";
cp ./alice/public ./bob/alice_pub;

read nil;

echo "\$ cp ./bob/public ./alice/alice_pub";
cp ./bob/public ./alice/bob_pub;

read nil;

ls -1R;

read nil;

echo "\$ python3 ../main.py genshared ./domain ./bob/private ./bob/alice_pub ./bob/shared";
read nil;
python3 ../main.py genshared ./domain ./bob/private ./bob/alice_pub ./bob/shared;


read nil;

echo "\$ python3 ../main.py genshared ./domain ./alice/private ./alice/bob_pub ./alice/shared";
read nil;
python3 ../main.py genshared ./domain ./alice/private ./alice/bob_pub ./alice/shared;
read nil;

echo -e "\n";
echo "\$ cat ./alice/shared";
cat ./alice/shared;
echo -e "\n";
echo "\$ cat ./bob/shared";
cat ./bob/shared;
echo -e "\n";
