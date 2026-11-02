-- Code extracted from the lab report (report.pdf)

-- ---- fragment 1 ----
SET @faculty_id = 3;
SET @min_amount = 50;
CALL facult_change(@faculty_id, @places, @min_amount);
SELECT @min_amount

-- ---- fragment 2 ----
        SET MESSAGE_TEXT = 'Places should be >0';
    END IF;

    UPDATE faculties

-- ---- fragment 3 ----
DECLARE counts INT DEFAULT 0;
DECLARE num_places INT DEFAULT 0;
DECLARE max_places INT;
DECLARE faculties_id INT;
DECLARE places_summ INT;
DECLARE faculty_name VARCHAR(100);
DECLARE result VARCHAR(100) DEFAULT '';

SELECT MAX(places) INTO max_places FROM faculties;
SELECT COUNT(*) FROM faculties INTO num_places;
SET counts = 0;

-- ---- fragment 4 ----
SET result = CONCAT(result, 'Faculty ID: ', faculties_id, ' Name:' , faculty_name ,', Places ', places_summ, '\n');
END IF;
SET counts = counts + 1;
END WHILE;
SELECT result AS outpust;
