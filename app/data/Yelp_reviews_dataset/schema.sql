CREATE TABLE business (
    business_id TEXT PRIMARY KEY,
    name TEXT,
    address TEXT,
    city TEXT,
    state TEXT,
    postal_code TEXT,
    latitude REAL,
    longitude REAL,
    stars REAL,
    review_count INTEGER,
    is_open INTEGER
);

CREATE TABLE review (
    review_id TEXT PRIMARY KEY,
    user_id TEXT,
    business_id TEXT,
    stars INTEGER,
    date TEXT,
    text TEXT,
    useful INTEGER,
    funny INTEGER,
    cool INTEGER,
    FOREIGN KEY (business_id) REFERENCES business (business_id)
);

CREATE TABLE "user" (  
    user_id TEXT PRIMARY KEY,
    name TEXT,
    review_count INTEGER,
    yelping_since TEXT,
    useful INTEGER,
    funny INTEGER,
    cool INTEGER,
    fans INTEGER,
    average_stars REAL,
    compliment_hot INTEGER,
    compliment_more INTEGER,
    compliment_profile INTEGER,
    compliment_cute INTEGER,
    compliment_list INTEGER,
    compliment_note INTEGER,
    compliment_plain INTEGER,
    compliment_cool INTEGER,
    compliment_funny INTEGER,
    compliment_writer INTEGER,
    compliment_photos INTEGER
);

CREATE TABLE checkin (
    checkin_id SERIAL PRIMARY KEY,
    business_id TEXT,
    date TEXT,
    FOREIGN KEY (business_id) REFERENCES business (business_id)
);

CREATE TABLE tip (
    tip_id SERIAL PRIMARY KEY,
    text TEXT,
    date TEXT,
    compliment_count INTEGER,
    business_id TEXT,
    user_id TEXT,
    FOREIGN KEY (business_id) REFERENCES business (business_id),
    FOREIGN KEY (user_id) REFERENCES "user" (user_id)  
);
