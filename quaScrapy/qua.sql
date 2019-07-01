CREATE TABLE IF NOT EXISTS `QUA_ATTRACTIONS`
(
  ID      VARCHAR(32),
  NAME    VARCHAR(512),
  PRICE   VARCHAR(16),
  SALES   VARCHAR(16),
  HEAT    VARCHAR(128),
  ADDRESS VARCHAR(512),
  SCORE   VARCHAR(16),
  PRIMARY KEY(`ID`)
) Engine=InnoDB DEFAULT CHARSET = utf8;

CREATE TABLE IF NOT EXISTS `QUA_EVALUATION`
(
  ID              VARCHAR(32),
  ITEM_ID          VARCHAR(32),
  EVALUATION_TYPE VARCHAR(16),
  EVALUATION_TEXT VARCHAR(128),
  AUTHOR          VARCHAR(128),
  CONTENT         VARCHAR(4000),
  CREATE_DATE      DATE,
  SCORE           VARCHAR(16),
  IMGS            VARCHAR(4000),
  USER_NICKNAME   VARCHAR(128),
  PRIMARY KEY (`ID`)
) Engine = InnoDB
  DEFAULT CHARSET = utf8;