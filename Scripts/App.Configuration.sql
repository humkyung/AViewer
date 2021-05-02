CREATE TABLE IF NOT EXISTS Configuration (
	"Section" TEXT NOT NULL,
	"Key" TEXT NOT NULL,
	Value TEXT,
	CONSTRAINT Configuration_PK PRIMARY KEY ("Section","Key")
);
