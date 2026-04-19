drop table if EXISTS transactions;
drop table if EXISTS products;
drop table if EXISTS accounts;

create table accounts(
    account_id INTEGER PRIMARY KEY,
    first_name VARCHAR(20) not null,
    last_name VARCHAR(20) not null,
    address_1 VARCHAR(255),
    address_2 VARCHAR(255),
    city VARCHAR(100),
    state VARCHAR(100),
    zip_code INTEGER,
    join_date DATE
);

create index idx_accounts_name on accounts(last_name, first_name);

create table products(
    product_id INTEGER PRIMARY KEY,
    product_code integer not null ,
    product_description text
);

create index idx_products_code on products(product_code);

create table transactions(
    transaction_id text PRIMARY KEY,
    transaction_date date not null,
    product_id INTEGER not NULL,
    product_code INTEGER,
    product_description text,
    quantity INTEGER,
    account_id INTEGER not NULL,
    
    constraint fk_product
        foreign key (product_id) REFERENCES products(product_id),

    constraint fk_accounts
        foreign key (account_id) REFERENCES accounts(account_id)
);

CREATE INDEX idx_transactions_product ON transactions(product_id);
CREATE INDEX idx_transactions_accounts ON transactions(account_id);
CREATE INDEX idx_transactions_date ON transactions(transaction_date);
