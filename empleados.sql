-- phpMyAdmin SQL Dump
-- version 4.6.6deb5
-- https://www.phpmyadmin.net/
--
-- Servidor: localhost:3306
-- Tiempo de generación: 25-06-2021 a las 11:15:55
-- Versión del servidor: 10.3.27-MariaDB-0+deb10u1
-- Versión de PHP: 7.3.27-1~deb10u1

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `empleados`
--
CREATE DATABASE IF NOT EXISTS `empleados` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
USE `empleados`;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `empleado`
--

CREATE TABLE `empleado` (
  `cedula` varchar(10) NOT NULL,
  `nombre` varchar(50) DEFAULT NULL,
  `apellido` varchar(50) DEFAULT NULL,
  `correo` varchar(50) DEFAULT NULL,
  `UU_ID` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Volcado de datos para la tabla `empleado`
--

INSERT INTO `empleado` (`cedula`, `nombre`, `apellido`, `correo`, `UU_ID`) VALUES
('12313', 'Matias ', 'Berni', 'maberni@fiuna.edu.py', '12'),
('12345', 'Juan', 'Perez', 'Jrpe@fokr.com', '15'),
('132123132', 'Jose', 'Benito', 'jbe@fiuna.com', '580422207102'),
('4187393', 'Franco', 'Maidana', 'maifranco@fiuna.edu.py', '1064169564585');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `registro_ent`
--

CREATE TABLE `registro_ent` (
  `idRegistro` int(11) NOT NULL,
  `hora_ent` varchar(50) DEFAULT NULL,
  `cedula` varchar(10) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Volcado de datos para la tabla `registro_ent`
--

INSERT INTO `registro_ent` (`idRegistro`, `hora_ent`, `cedula`) VALUES
(1, '18:50:33', '132123132');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `tarjeta`
--

CREATE TABLE `tarjeta` (
  `UU_ID` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Volcado de datos para la tabla `tarjeta`
--

INSERT INTO `tarjeta` (`UU_ID`) VALUES
('.!toplevel.!entry5'),
('1064169564585'),
('12'),
('15'),
('580422207102');

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `empleado`
--
ALTER TABLE `empleado`
  ADD PRIMARY KEY (`cedula`),
  ADD KEY `UU_ID` (`UU_ID`);

--
-- Indices de la tabla `registro_ent`
--
ALTER TABLE `registro_ent`
  ADD PRIMARY KEY (`idRegistro`),
  ADD KEY `cedula` (`cedula`);

--
-- Indices de la tabla `tarjeta`
--
ALTER TABLE `tarjeta`
  ADD PRIMARY KEY (`UU_ID`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `registro_ent`
--
ALTER TABLE `registro_ent`
  MODIFY `idRegistro` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;
--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `empleado`
--
ALTER TABLE `empleado`
  ADD CONSTRAINT `empleado_ibfk_1` FOREIGN KEY (`UU_ID`) REFERENCES `tarjeta` (`UU_ID`);

--
-- Filtros para la tabla `registro_ent`
--
ALTER TABLE `registro_ent`
  ADD CONSTRAINT `registro_ent_ibfk_1` FOREIGN KEY (`cedula`) REFERENCES `empleado` (`cedula`);

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
