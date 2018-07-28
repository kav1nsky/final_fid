#include <eosiolib/eosio.hpp>

class fidelity : public eosio::contract {
    public:
        fidelity( account_name self ):contract(self) {}

        /*
        @brief Information related to employee account
        @abi table workers i64
        */
        struct worker {
            account_name account;
            std::string name;
            std::vector<std::string> info;
            std::vector<uint64_t> recordIds;
            std::vector<uint64_t> agreementIds;

            static const uint16_t nameMaxLength = 100;
            static const uint16_t infoMaxLength = 500;

            auto primary_key() const { return account; }
            EOSLIB_SERIALIZE(worker, (account)(name)(info)(recordIds)(agreementIds))
        };
        typedef eosio::multi_index<N(workers), worker> workers;

        /*
        @brief Information related to customer account_name
        @abi table customers i64
        */
        struct customer {
            account_name account;
            std::string name;
            std::string info;
            std::vector<uint64_t> recordIds;
            std::vector<uint64_t> agreementIds;

            static const uint16_t nameMaxLength = 100;
            static const uint16_t infoMaxLength = 1000;

            auto primary_key() const { return account; }
            EOSLIB_SERIALIZE(customer, (account)(name)(info)(recordIds)(agreementIds))
        };
        typedef eosio::multi_index<N(customers), customer> customers;

        /*
        @brief Information related to record
        @abi table records i64
        */
        struct record {
            uint64_t id;
            account_name authorName;
            account_name targetName;
            uint16_t rating;
            std::string comment;

            static const uint16_t commentMaxLength = 500;

            auto primary_key() const { return id; }
            EOSLIB_SERIALIZE(record, (id)(authorName)(targetName)(rating)(comment))
        };
        typedef eosio::multi_index<N(records), record> records;

        /*
        @brief Information related to agreementIds
        @abi table agreements i64
        */
        struct agreement {
            uint64_t id;
            account_name workerName;
            account_name customerName;
            std::string content;
            time due;
            uint16_t state; // 0 - Offered, 1 - Accepted, 2 - Rejected, 3 - Finished & Rated by Customer, 4 - Finished & Rated by Worker, 5 - Finished & Rated by Both

            static const uint16_t contentMaxLength = 1000;

            auto primary_key() const { return id; }
            EOSLIB_SERIALIZE(agreement, (id)(workerName)(customerName)(content)(due)(state))
        };
        typedef eosio::multi_index<N(agreements), agreement> agreements;

        // Account management actions

        // @abi action
        void setworker(const account_name& account, const std::string& name);

        // @abi action
        void addinfo(const account_name& account, const std::string& infoContent);

        // @abi action
        void setcustomer(const account_name& account, const std::string& name, const std::string& info);

        // Agreement management actions

        // @abi action
        void initagr(const account_name& customerName, const account_name& workerName, const std::string& content, const time& due);

        // @abi action
        void acceptagr(const account_name& account, const uint64_t& id);

        // @abi action
        void rejectagr(const account_name& account, const uint64_t& id);

        // Records management actions

        // @abi action
        void putrecord(const account_name& account, const uint64_t& agreementId, const uint16_t rating, const std::string& comment);
};
