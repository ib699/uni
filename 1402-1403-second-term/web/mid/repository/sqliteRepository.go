package repository

import (
	"database/sql"
	"errors"
	"github.com/ib699/mid/model"
)

var (
	ErrDuplicate    = errors.New("record already exists")
	ErrNotExists    = errors.New("row not exists")
	ErrUpdateFailed = errors.New("update failed")
	ErrDeleteFailed = errors.New("delete failed")
)

type SQLiteRepository struct {
	Db *sql.DB
}

func NewSQLiteRepository(db *sql.DB) *SQLiteRepository {
	return &SQLiteRepository{Db: db}
}

func (r *SQLiteRepository) InitBasket() error {
	query := `
    CREATE TABLE IF NOT EXISTS baskets(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user TEXT NOT NULL,
        created_at TEXT NOT NULL,
        updated_at TEXT NOT NULL,
        basketData TEXT NOT NULL,
        status TEXT NOT NULL
    );
    `

	_, err := r.Db.Exec(query)
	return err
}

func (r *SQLiteRepository) CreateBasket(basket model.Basket) (*model.Basket, error) {
	res, err := r.Db.Exec("INSERT INTO baskets(created_at, user, updated_at, basketData, status) values(?,?,?,?,?)", basket.CreatedAt, basket.User, basket.UpdatedAt, basket.BasketData, basket.Status)
	if err != nil {
		return nil, err
	}

	id, err := res.LastInsertId()
	if err != nil {
		return nil, err
	}
	basket.ID = id

	return &basket, nil
}

func (r *SQLiteRepository) AllBasket() ([]model.Basket, error) {
	rows, err := r.Db.Query("SELECT * FROM baskets")
	if err != nil {
		return nil, err
	}
	defer rows.Close()

	var all []model.Basket
	for rows.Next() {
		var basket model.Basket
		if err := rows.Scan(&basket.ID, &basket.User, &basket.CreatedAt, &basket.UpdatedAt, &basket.BasketData, &basket.Status); err != nil {
			return nil, err
		}
		all = append(all, basket)
	}
	return all, nil
}

func (r *SQLiteRepository) GetByIdBasket(id int64) (*model.Basket, error) {
	row := r.Db.QueryRow("SELECT * FROM baskets WHERE id = ?", id)

	var basket model.Basket
	if err := row.Scan(&basket.ID, &basket.User, &basket.CreatedAt, &basket.UpdatedAt, &basket.BasketData, &basket.Status); err != nil {
		if errors.Is(err, sql.ErrNoRows) {
			return nil, ErrNotExists
		}
		return nil, err
	}
	return &basket, nil
}

func (r *SQLiteRepository) GetByNameBasket(name string) ([]model.Basket, error) {
	rows, err := r.Db.Query("SELECT * FROM baskets WHERE user = ?", name)
	if err != nil {
		return nil, err
	}
	defer rows.Close()

	var all []model.Basket
	for rows.Next() {
		var basket model.Basket
		if err := rows.Scan(&basket.ID, &basket.User, &basket.CreatedAt, &basket.UpdatedAt, &basket.BasketData, &basket.Status); err != nil {
			return nil, err
		}
		all = append(all, basket)
	}
	return all, nil
}

func (r *SQLiteRepository) UpdateBasket(id int64, updated model.Basket) (*model.Basket, error) {
	if id == 0 {
		return nil, errors.New("invalid updated ID")
	}
	res, err := r.Db.Exec("UPDATE baskets SET user = ?, created_at = ?, updated_at = ?, basketData = ?, status = ? WHERE id = ?", updated.User, updated.CreatedAt, updated.UpdatedAt, updated.BasketData, updated.Status, id)
	if err != nil {
		return nil, err
	}

	rowsAffected, err := res.RowsAffected()
	if err != nil {
		return nil, err
	}

	if rowsAffected == 0 {
		return nil, ErrUpdateFailed
	}

	return &updated, nil
}

func (r *SQLiteRepository) DeleteBasket(id int64) error {
	res, err := r.Db.Exec("DELETE FROM baskets WHERE id = ?", id)
	if err != nil {
		return err
	}

	rowsAffected, err := res.RowsAffected()
	if err != nil {
		return err
	}

	if rowsAffected == 0 {
		return ErrDeleteFailed
	}

	return nil
}

func (r *SQLiteRepository) InitUser() error {
	query := `
    CREATE TABLE IF NOT EXISTS users(
		id INTEGER PRIMARY KEY AUTOINCREMENT,
		username TEXT NOT NULL,
		password TEXT NOT NULL
	);
    `

	_, err := r.Db.Exec(query)
	return err
}

func (r *SQLiteRepository) CreateUser(user model.User) (*model.User, error) {
	res, err := r.Db.Exec("INSERT INTO users(username, password) VALUES(?, ?)", user.Username, user.Password)
	if err != nil {
		return nil, err
	}

	id, err := res.LastInsertId()
	if err != nil {
		return nil, err
	}
	user.ID = id

	return &user, nil
}

func (r *SQLiteRepository) CheckUserName(name string) error {
	row := r.Db.QueryRow("SELECT * FROM users WHERE username = ?", name)

	var user model.User
	if err := row.Scan(&user.ID, &user.Username, &user.Password); err != nil {
		if errors.Is(err, sql.ErrNoRows) {
			return ErrNotExists
		}
		return err
	}
	return nil
}

func (r *SQLiteRepository) GetUser(name string) (*model.User, error) {
	row := r.Db.QueryRow("SELECT * FROM users WHERE username = ?", name)

	var user model.User
	if err := row.Scan(&user.ID, &user.Username, &user.Password); err != nil {
		if errors.Is(err, sql.ErrNoRows) {
			return nil, ErrNotExists
		}
		return nil, err
	}
	return &user, nil
}

func (r *SQLiteRepository) UpdateUser(id int64, updated model.User) (*model.User, error) {
	if id == 0 {
		return nil, errors.New("invalid updated ID")
	}
	res, err := r.Db.Exec("UPDATE users SET username = ?, password = ? WHERE id = ?", updated.Username, updated.Password, id)
	if err != nil {
		return nil, err
	}

	rowsAffected, err := res.RowsAffected()
	if err != nil {
		return nil, err
	}

	if rowsAffected == 0 {
		return nil, ErrUpdateFailed
	}

	return &updated, nil
}

func (r *SQLiteRepository) DeleteUserByName(name string) error {
	res, err := r.Db.Exec("DELETE FROM users WHERE username = ?", name)
	if err != nil {
		return err
	}

	rowsAffected, err := res.RowsAffected()
	if err != nil {
		return err
	}

	if rowsAffected == 0 {
		return ErrDeleteFailed
	}

	return nil
}
