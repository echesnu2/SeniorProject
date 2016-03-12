CREATE TABLE IF NOT EXISTS `mydb`.`useractivity` (
  `userid` INT(11) NOT NULL,
  `activityid` INT(11) NOT NULL,
  PRIMARY KEY (`userid`, `activityid`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8
COMMENT = ''/*This is a Association entity, since Activity - User is a many to many relationship, use this to find activities and users matching.
To find activities for a user, do something like: SELECT FROM UserActivity WHERE USER.id = X
To find users on a specific activity, do something like: SELECT FROM UserActivity WHERE Activity.id = X*/