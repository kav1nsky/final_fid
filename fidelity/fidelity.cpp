#include <fidelity.hpp>

using namespace eosio;

// Account management actions

// @abi action
void fidelity::setworker(const account_name& account, const std::string& name) {
    require_auth(account);

    workers allWorkers(_self, _self);
    auto itr = allWorkers.find(account);

    if (itr != allWorkers.end()) {
        allWorkers.modify(itr, _self, [&]( auto& w ) {
            w.name = name;
        });
    }
    else {
        allWorkers.emplace(account, [&]( auto& w ) {
            w.account = account;
            w.name = name;
            w.info = std::vector<std::string>(0);
            w.recordIds = std::vector<uint64_t>(0);
            w.agreementIds = std::vector<uint64_t>(0);
        });
    }
}

// @abi action
void fidelity::addinfo(const account_name& account, const std::string& infoContent) {
    require_auth(account);

    workers allWorkers(_self, _self);
    auto itr = allWorkers.find(account);
    eosio_assert(itr != allWorkers.end(), "There is no such worker");

    allWorkers.modify(itr, _self, [&]( auto& w ) {
        w.info.push_back(infoContent);
    });
}

// @abi action
void fidelity::setcustomer(const account_name& account, const std::string& name, const std::string& info) {
    require_auth(account);

    customers allCustomers(_self, _self);
    auto itr = allCustomers.find(account);

    if (itr != allCustomers.end()) {
        allCustomers.modify(itr, itr->account, [&]( auto& c ) {
            c.name = name;
            c.info = info;
        });
    }
    else {
        allCustomers.emplace(account, [&]( auto& c ) {
            c.account = account;
            c.name = name;
            c.info = info;
            c.recordIds = std::vector<uint64_t>(0);
            c.agreementIds = std::vector<uint64_t>(0);
        });
    }
}

// Agreement management actions

// @abi action
void fidelity::initagr(const account_name& customerName, const account_name& workerName, const std::string& content, const time& due) {
    require_auth(customerName);

    customers allCustomers(_self, _self);
    auto itr = allCustomers.find(customerName);
    eosio_assert(itr != allCustomers.end(), "There is no such customer");

    workers allWorkers(_self, _self);
    auto itr2 = allWorkers.find(workerName);
    eosio_assert(itr2 != allWorkers.end(), "There is no such worker");

    agreements allAgreements(_self, _self);
    auto newId = allAgreements.available_primary_key();

    print(newId);

    allAgreements.emplace(_self, [&]( auto& a ) {
        a.id = newId;
        a.customerName = customerName;
        a.workerName = workerName;
        a.content = content;
        a.due = due;
        a.state = 0;
    });

    allCustomers.modify(itr, _self, [&]( auto& c ) {
        c.agreementIds.push_back(newId);
    });

    allWorkers.modify(itr2, _self, [&]( auto& w ) {
        w.agreementIds.push_back(newId);
    });
}

// @abi action
void fidelity::acceptagr(const account_name& account, const uint64_t& id) {
    require_auth(account);

    agreements allAgreements(_self, _self);
    auto itr = allAgreements.find(id);
    eosio_assert(itr != allAgreements.end(), "There is no such agreement");
    eosio_assert(itr->state == 0, "Agreement was already accepted or rejected");
    eosio_assert(account == itr->workerName, "Only agreement worker can accept it");

    allAgreements.modify(itr, _self, [&]( auto& a ) {
        a.state = 1;
    });
}

// @abi action
void fidelity::rejectagr(const account_name& account, const uint64_t& id) {
    require_auth(account);

    agreements allAgreements(_self, _self);
    auto itr = allAgreements.find(id);
    eosio_assert(itr != allAgreements.end(), "There is no such agreement");
    eosio_assert(itr->state == 0, "Agreement was already accepted or rejected");
    eosio_assert(account == itr->workerName || account == itr->customerName, "Only agreement worker or customer can reject it");

    allAgreements.modify(itr, _self, [&]( auto& a ) {
        a.state = 2;
    });
}

// Records management actions

// @abi action
void fidelity::putrecord(const account_name& account, const uint64_t& agreementId, const uint16_t rating, const std::string& comment) {
    require_auth(account);

    agreements allAgreements(_self, _self);
    auto itr = allAgreements.find(agreementId);

    eosio_assert(now() >= itr->due, "Agreement isn't finished yet");

    records allRecords(_self, _self);

    if (account == itr->customerName && (itr->state == 1 || itr->state == 4)) {
        allAgreements.modify(itr, _self, [&]( auto& a ) {
            a.state = itr->state == 1 ? 3 : 5;
        });

        auto newId = allRecords.available_primary_key();

        print(newId);

        allRecords.emplace(_self, [&]( auto& r ) {
            r.id = newId;
            r.authorName = account;
            r.targetName = itr->workerName;
            r.rating = rating;
            r.comment = comment;
        });

        workers allWorkers(_self, itr->workerName);
        auto itr2 = allWorkers.find(itr->workerName);

        allWorkers.modify(itr2, _self, [&]( auto& w ) {
            w.recordIds.push_back(newId);
        });
    } else if (account == itr->workerName && (itr->state == 1 || itr->state == 3)) {
        allAgreements.modify(itr, _self, [&]( auto& a ) {
            a.state = itr->state == 1 ? 4 : 5;
        });

        auto newId = allRecords.available_primary_key();

        print(newId);

        allRecords.emplace(_self, [&]( auto& r ) {
            r.id = newId;
            r.authorName = account;
            r.targetName = itr->customerName;
            r.rating = rating;
            r.comment = comment;
        });

        customers allCustomers(_self, itr->customerName);
        auto itr2 = allCustomers.find(itr->customerName);

        allCustomers.modify(itr2, _self, [&]( auto& c ) {
            c.recordIds.push_back(newId);
        });
    }
}

EOSIO_ABI(fidelity, (setworker)(addinfo)(setcustomer)(initagr)(acceptagr)(rejectagr)(putrecord))
