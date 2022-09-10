-- --------------------------------------------------------
-- Host:                         127.0.0.1
-- Server version:               10.6.0-MariaDB - mariadb.org binary distribution
-- Server OS:                    Win64
-- HeidiSQL Version:             11.2.0.6213
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


-- Dumping database structure for biblioteca
DROP DATABASE IF EXISTS `biblioteca`;
CREATE DATABASE IF NOT EXISTS `biblioteca` /*!40100 DEFAULT CHARACTER SET latin1 */;
USE `biblioteca`;

-- Dumping structure for table biblioteca.libros
DROP TABLE IF EXISTS `libros`;
CREATE TABLE IF NOT EXISTS `libros` (
  `idLibro` int(11) NOT NULL AUTO_INCREMENT,
  `nombreLibro` varchar(50) DEFAULT NULL,
  `prestado` int(50) DEFAULT NULL,
  `fecha` date DEFAULT NULL,
  PRIMARY KEY (`idLibro`)
) ENGINE=InnoDB AUTO_INCREMENT=28 DEFAULT CHARSET=latin1;

-- Dumping data for table biblioteca.libros: ~13 rows (approximately)
/*!40000 ALTER TABLE `libros` DISABLE KEYS */;
REPLACE INTO `libros` (`idLibro`, `nombreLibro`, `prestado`, `fecha`) VALUES
	(4, 'after', 5, '2021-06-06'),
	(5, 'fluyan mis lagrimas', 0, '0000-00-00'),
	(6, 'ubik', 16, '2021-05-29'),
	(10, 'hobbit', 0, '0000-00-00'),
	(11, 'ready player one', 0, '0000-00-00'),
	(13, 'harry potter', 0, '0000-00-00'),
	(14, 'valis', 0, '0000-00-00'),
	(15, 'el atlas de las nubes', 0, '0000-00-00'),
	(16, 'fundacion', 12, '2021-06-12'),
	(17, '1984', 0, '0000-00-00'),
	(18, 'el corredor del laberinto', 0, '0000-00-00'),
	(19, 'seis cuervos', 0, '0000-00-00');
/*!40000 ALTER TABLE `libros` ENABLE KEYS */;

-- Dumping structure for table biblioteca.roles
DROP TABLE IF EXISTS `roles`;
CREATE TABLE IF NOT EXISTS `roles` (
  `idRol` int(11) NOT NULL AUTO_INCREMENT,
  `nombreRol` varchar(50) NOT NULL DEFAULT '',
  `agregarLibro` char(1) NOT NULL DEFAULT 'N',
  `buscarLibro` char(1) NOT NULL DEFAULT 'N',
  `eliminarLibro` char(1) NOT NULL DEFAULT 'N',
  `añadirCliente` char(1) NOT NULL DEFAULT 'N',
  `buscarUsuario` char(1) NOT NULL DEFAULT 'N',
  `prestarLibro` char(1) NOT NULL DEFAULT 'N',
  `devolucionLibro` char(1) NOT NULL DEFAULT 'N',
  `añadirBibliotecario` char(1) NOT NULL DEFAULT 'N',
  `despedirBibliotecario` char(1) NOT NULL DEFAULT 'N',
  `enviarEmail` char(1) NOT NULL DEFAULT 'N',
  `ficheroCSV` char(1) DEFAULT 'N',
  PRIMARY KEY (`idRol`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=latin1;

-- Dumping data for table biblioteca.roles: ~3 rows (approximately)
/*!40000 ALTER TABLE `roles` DISABLE KEYS */;
REPLACE INTO `roles` (`idRol`, `nombreRol`, `agregarLibro`, `buscarLibro`, `eliminarLibro`, `añadirCliente`, `buscarUsuario`, `prestarLibro`, `devolucionLibro`, `añadirBibliotecario`, `despedirBibliotecario`, `enviarEmail`, `ficheroCSV`) VALUES
	(1, 'admin', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S'),
	(2, 'bibliotecario', 'S', 'S', 'S', 'S', 'N', 'S', 'S', 'N', 'N', 'N', 'N'),
	(3, 'cliente', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N');
/*!40000 ALTER TABLE `roles` ENABLE KEYS */;

-- Dumping structure for table biblioteca.usuarios
DROP TABLE IF EXISTS `usuarios`;
CREATE TABLE IF NOT EXISTS `usuarios` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(50) DEFAULT NULL,
  `rol` int(11) DEFAULT NULL,
  `userID` varchar(50) DEFAULT NULL,
  `contraseña` varchar(80) DEFAULT NULL,
  `correo` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=46 DEFAULT CHARSET=latin1;

-- Dumping data for table biblioteca.usuarios: ~10 rows (approximately)
/*!40000 ALTER TABLE `usuarios` DISABLE KEYS */;
REPLACE INTO `usuarios` (`id`, `nombre`, `rol`, `userID`, `contraseña`, `correo`) VALUES
	(0, 'disponible', NULL, NULL, NULL, NULL),
	(1, 'admin', 1, 'p', '*E6CC90B878B948C35E92B003C792C46C58C4AF40', NULL),
	(2, 'bibliotecario', 2, 'a', '*E6CC90B878B948C35E92B003C792C46C58C4AF40', NULL),
	(3, 'user', 2, 'h', '*E6CC90B878B948C35E92B003C792C46C58C4AF40', 'vicendmg@gmail.com'),
	(5, 'marta', 2, NULL, NULL, NULL),
	(12, 'marcos', 3, NULL, NULL, NULL),
	(16, 'alba', 3, NULL, NULL, NULL),
	(43, 'david', 3, NULL, NULL, ''),
	(44, 'pablo', 3, NULL, NULL, ''),
	(45, 'andres', 3, NULL, NULL, '');
/*!40000 ALTER TABLE `usuarios` ENABLE KEYS */;

/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;
