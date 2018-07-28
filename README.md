# Fidelity
Fidellity Digital Passport

# Развертка EOS

Сначала необходимо скачать EOS и запустить ноды
1. Скачать EOS в соответствии с https://developers.eos.io/eosio-nodeos/docs/getting-the-code
2. Сбилдить EOS в соответствии с https://developers.eos.io/eosio-nodeos/docs/autobuild-script
3. Добавить исполняемые файлы в соответствии с https://developers.eos.io/eosio-nodeos/docs/install-executables и убедиться, что команды nodeos, cleos доступны из терминала 
3. Запустить ноду командой  nodeos --plugin eosio::wallet_api_plugin --plugin eosio::wallet_plugin --plugin eosio::producer_plugin --plugin eosio::history_plugin --plugin eosio::chain_api_plugin --plugin eosio::history_api_plugin --plugin eosio::http_plugin --replay-blockchain --hard-replay-blockchain --delete-all-blocks --enable-stale-production --producer-name eosio --contracts-console

Затем необходимо создать аккаунты  
(Все действия в терминале)  
cleos create wallet (вернет пароль, его нужно сохранить)  
cleos wallet open  
cleos wallet unlock (ввести пароль)  
cleos create key (вернет публичный и приватный ключи, сохранить оба)  
cleos wallet import [privatekey]  
cleos create account eosio test [publickey]  
cleos create accounts eosio contract [public key]

Затем нужно запустить контракт  
(Все действия в терминале из корневой директории репозитория)  
eosiocpp -o Contract.wast Contract.cpp   
eosiocpp -g Contract.abi Contract.cpp  
cleos set contract contract ../Contract  

Проверим, что все работает (из терминала)  
cleos push action contract hi ['test'] -p test@active  

Должно вывестись (в числе прочего) "Hello, test"  
