# Premium Lucky
This project contains a premium bond result file parser and aiohttp web server.
The premium bond parser can parse the results files which can be downloaded on the 
[NS&I Website](https://www.nsandi.com/prize-checker)

## Parser
The parser is a simple generator which takes a file and spits out a tuple containing
the bond number, prize and winning month.

## Server
The server is aiohttp application making using of Postgres and GINO as an ORM.
The server contains three routes one for looking on the winning history of the bond, one for the bonds 
which have won the largest amount and another for bonds which have won most frequently.