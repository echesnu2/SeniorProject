CREATE TABLE IF NOT EXISTS `mydb`.`activity` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(45) NULL DEFAULT NULL,
  `skill` INT(11) NULL DEFAULT NULL,
  `datetime` DATETIME NOT NULL,
  `duration` INT(11) NULL DEFAULT NULL,
  `numplayers` INT(11) NOT NULL,
  `private` TINYINT(1) NOT NULL,
  `available` TINYINT(1) NOT NULL,
  `category` INT(11) NOT NULL,
  `leader` INT(11) NOT NULL,
  `latitude` DECIMAL(7,4) NULL,
  `longitude` DECIMAL(7,4) NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `id_UNIQUE` (`id` ASC),
  INDEX `category_idx` (`category` ASC),
  INDEX `leader_idx` (`leader` ASC),
  CONSTRAINT `category`
    FOREIGN KEY (`category`)
    REFERENCES `mydb`.`activitytype` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `leader`
    FOREIGN KEY (`leader`)
    REFERENCES `mydb`.`user` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
AUTO_INCREMENT = 7
DEFAULT CHARACTER SET = utf8