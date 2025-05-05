#!/bin/bash

rm ./domain

cp ./alice/private ./;
rm -r ./alice/;
mkdir alice;
mv ./private ./alice/private;

cp ./bob/private ./;
rm -r ./bob/;
mkdir bob;
mv ./private ./bob/private;


