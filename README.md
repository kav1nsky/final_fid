# Fidelity
Fidellity Digital Passport

## Развертка EOS

Установка EOS (проверено под Ubuntu 18.04, для других OS могут потребоваться дополнительные действия): 
```bash
git clone https://github.com/EOSIO/eos --recursive  
cd eos  
./eosio_build.sh # займет довольно много времени и ресурсов
cd build  
sudo make install 
```

После этого необходимо зайти в ~/.profile и добавить туда следующие строки:  
```bash
if [ -d "/usr/local/eosio/bin" ] ; then  
    PATH="/usr/local/eosio/bin:$PATH"  
fi  
```
Затем необходимо перезапустить компьютер, чтобы путь обновился.

Теперь необходимые компоненты EOS должны быть установлены. Можно проверить это, набрав в консоли cleos (если выведется сообщение со списком команд, то все в порядке)

Следующий шаг - запустить ноду EOS (локальный приватный блокчейн):
```bash
nodeos --plugin eosio::wallet_api_plugin --plugin eosio::wallet_plugin --plugin eosio::producer_plugin --plugin eosio::history_plugin --plugin eosio::chain_api_plugin --plugin eosio::history_api_plugin --plugin eosio::http_plugin --replay-blockchain --hard-replay-blockchain --delete-all-blocks --enable-stale-production --producer-name eosio --contracts-console
```
Если все в порядке, то нода начнет производить блоки каждые 0,5 секунды (будет появляться сообщение с номером нового блока)

Теперь к ноде должно быть возможно обращаться через cleos:
```bash
cleos get info
```
В ответ должен прийти JSON с информацией про текущий блокчейн

Теперь необходимо создать и подготовить кошелек, выполнив следующие команды:
```bash
cleos wallet create # вернет пароль, его нужно сохранить
cleos wallet open
cleos wallet unlock --password [wallet password] # использовать полученный пароль
cleos create key # вернет приватный и публичный ключи, их надо сохранить
cleos wallet import --private-key [private key] # использовать полученный приватный ключ
cleos wallet import --private-key 5KQwrPbwdL6PhXujxW37FSSQZ1JiwsST4cqQzDeyXtP79zkvFD3 # импортирует системный аккаунт eosio
cleos create account eosio contract [public key] # использовать полученный три шага назад публичный ключ
cleos create account eosio test [public key]
```

Теперь, наконец, можно сбилдить и задеплоить контракт (команды выполнять, зайдя в репозиторий проекта):
```bash
cd fidelity
./deploy [password]
cleos push action contract setworker '["test", "Tester Fidelity"]' -p test@active
cleos get table contract contract workers
```
Если все в порядке, то последняя команда вернет JSON, где будет объект работника, созданный предыдущей командой.

Также можно воспользоваться набором реализованных тестов, проверяющих работу основных методов смарт-контракта (команды выполнять из корневой директории проекта):
```bash
cd fidelity
python3 test_newfidelity.py
```
При выполнении тестов нужно будет последовательно ввести названия двух аккаунтов EOS, которые будут созданы в процессе выполнения тестов (это должны быть корректные названия, из строчных латинских букв и цифр от 1 до 5, не более 12 символов). 

## Интерфейс смарт-контракта

```cpp 
void setworker(const account_name& account, const std::string& name); 
```  
Действие принимает название текущего аккаунта (от которого вызывается) и имя пользователя (в естесственном языке). Оно либо создает для пользователя объект работника в смарт-контракте, либо обновляет имя уже существующего.

```cpp 
void addinfo(const account_name& account, const std::string& infoContent); 
```  
Действие принимает название текущего аккаунта (для которого уже должен быть создан объект работника) и строку с описанием некоторого опыта этого работника (образование, опыт работы, сертификат и т.д.), добавляя ее в базу данных смарт-контракта.

```cpp 
void setcustomer(const account_name& account, const std::string& name, const std::string& info); 
```
Действие принимает название текущего аккаунта, строку с названием клиента (под клиентом подразумевается лицо, в конечном итоге выставляющее оценки работнику, это может быть как и заказчик/работодатель, так и например университет) и описание этого клиента. Оно либо создает в смарт-контракте для данного аккаунта объект клиента, либо обновляет данные уже существующего.

```cpp 
void initagr(const account_name& customerName, const account_name& workerName, const std::string& content, const time& due); 
```
Действие, доступное только клиенту. Принимает название аккаунта этого клиента, название аккаунта работника, описание договора и срок окончания договора. Предлагает указанному работнику заключить описанный договор.

```cpp
void acceptagr(const account_name& account, const uint64_t& id); 
```
Действие, доступное только работнику. Принимает название текущего аккаунта и id договора, предложенного этому работнику (и пока еще не подтвержденного и не отвергнутого) и подтверждает его. 

```cpp
void rejectagr(const account_name& account, const uint64_t& id);
```
Действие, принимающее название текущего аккаунта и id некоторого договора (причем доступно только автору этого договора и работнику, которому он предложен, а также договор не должен быть подтвержден или отвергнут). Отвергает этот договор.

```cpp
void putrecord(const account_name& account, const uint64_t& agreementId, const uint16_t rating, const std::string& comment);
```
Действие, принимающее название текущего аккаунта, id договора (аккаунт должен быть участником этого договора, договор должен быть подтвержден и его срок должен истечь, этот аккаунт еще не должен был ставить по этому договору отзыв), числовое знание от 1 до 10, соответствующее оценке и текстовый комментарий об этой оценке. Оставляет партнеру по указанному договору отзыв с указанной оценкой и комментарием, записывая его в блокчейн. 

## Python библиотека

Для удобства взаимодействия со смарт-контрактом написана библиотека на python (/fidelity/newfidelity.py), которая позволяет обращаться к нему, используя функции python.

Для использования библиотеки нужно сначала создать в своем python-файле класс Fidelity:
```python
from fidelity import Fidelity
f = Fidelity([local eos wallet password]) # использовать пароль от предварительно созданного кошелька
```

Затем можно использовать следующие методы:
```python
f.createAccount(account_name) # создает новую пару ключей и аккаунт с этим ключом и указанным именем
f.setWorker(account, name)
f.getWorker(account)
f.addInfo(account, info)
f.setCustomer(account, name, info)
f.getCustomer(account)
f.initAgreement(account, target, content, die)
f.acceptAgreement(account, id)
f.rejectAgreement(account, id)
f.getAgreement(account, id)
f.putRecord(account, agreementId, rating, comment)
f.getRecord(account, recordId)
```
