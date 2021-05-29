USE tgbot;
-- DROP TABLE rates;
-- DROP TABLE forms;
-- DROP TABLE users;

-- CREATE TABLE users (
--     id INT PRIMARY KEY,
--     registration_date DATE,
--     last_active DATE
-- );

CREATE TABLE forms (
    id INT PRIMARY KEY,
    name VARCHAR(100),
    year YEAR(4),
    gender VARCHAR(100),
    city VARCHAR(100),
    info VARCHAR(10000),
    image LONGBLOB,
    isActive BOOl,
    lastActive DATE,
    popularity INT,
    FOREIGN KEY (id) REFERENCES users (id) ON DELETE CASCADE
);

CREATE TABLE rates (
    id_subject INT,
    id_object INT,
    text_message VARCHAR(100),
    PRIMARY KEY (id_subject, id_object),
    FOREIGN KEY (id_subject) REFERENCES users (id) ON DELETE CASCADE,
    FOREIGN KEY (id_object) REFERENCES users (id) ON DELETE CASCADE
);
