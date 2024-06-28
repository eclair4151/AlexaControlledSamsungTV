class Init < ActiveRecord::Migration[5.1]
  def change
    
    create_table :users do |t|
      t.text :email
      t.text :first_name
      t.text :last_name
      t.text :password_digest
      t.timestamps
    end
    
    
    create_table :devices do |t|
      t.text :name
      t.boolean :deleted, null: false, default: 'f'
      t.text :location
      t.text :uuid
      t.text :private_key
      t.text :pubic_certificate
      t.datetime :last_pinged
      t.timestamps
    end
    
    create_table :tvs do |t|
      t.text :name
      t.text :mac_address
      t.text :model_number
      t.timestamps
    end
    
    add_reference :devices, :user, foreign_key: true
    add_reference :tvs, :device, foreign_key: true
    add_index :devices, :uuid, unique: true
    add_index :users, :email, unique: true

  end
end
