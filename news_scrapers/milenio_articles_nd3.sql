SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";

CREATE TABLE IF NOT EXISTS `milenio_articles_nd1` (
`id` int(8) NOT NULL,
  `url` varchar(250) NOT NULL,
  `timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `title` varchar(200) NOT NULL,
  `pubdate` varchar(30) NOT NULL,
  `city` varchar(30) NOT NULL,
  `article` text NOT NULL,
  `filtered_article` text NOT NULL,
  `section` varchar(30) NOT NULL,
  `sentimient` set('g','b','n') NOT NULL
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=40073 ;

--
-- Dumping data for table `milenio_articles_nd1`
--

INSERT INTO `milenio_articles_nd1` (`id`, `url`, `timestamp`, `title`, `pubdate`, `city`, `article`, `filtered_article`, `section`, `sentimient`) VALUES
(1, 'http://com.milenio.feedsportal.com/c/33388/f/600778/s/391a35af/sc/7/l/0L0Smilenio0N0Cdf0Clinea0I120Idel0Imetro0Elinea0I120Esuspenden0Ilinea0I120Emetro0Ilinea0I120Edebate0Iperitos0I0A0I27657290A50Bhtml/story01.htm', '2014-07-09 13:48:36', 'Debate técnico de peritos arrojará conclusiones sobre L12: ALDF', 'Tue, 08 Apr 2014 01:46:59 GMT', 'Ciudad de México', '\n  Este viernes concluirán las comparecencias relacionadas con las fallas que presentó la Línea 12 del Metro y que ocasionaron la suspensión del servicio en 11 estaciones, y entonces se definirá la fecha o las fechas para un debate técnico entre peritos, a fin de llegar a una conclusión sobre las causas y las probables responsabilidades.Lo anterior informó a MILENIO Televisión el presidente de la Comisión Especial que investiga dichas fallas de la Línea Dorada del Sistema de Transporte Colectivo Metro, Jorge Gaviño, quien aseguró que se armará el rompecabezas tras las comparecencias de siete grupos involucrados en el tema, de las cuales "hay puntos que se contradicen de manera muy grave".Dijo que supervisoras de las obras civil y electromecánica de la Línea 12 serán las últimas comparecientes ante esa comisión de la Asamblea Legislativa del Distrito Federal.Una vez que hayan concluido las reuniones con las partes involucradas en la construcción de esa línea, es decir, siete grupos, dijo, se tendrán los elementos de todas ellas y "tendremos el rompecabezas".Gaviño refirió que se han conocido puntos torales de la investigación, pero algunos "se contradicen de manera muy grave", como es el caso de quienes dicen que los trenes son incompatibles con las vías, y otros que son "perfectamente compatibles".Hay visiones de que si fueran incompatibles, no funcionaría la otra mitad de la Línea 12, y también hay quienes aseguran que hubo descuido en el mantenimiento de la misma, expuso.El diputado local dijo que las aseveraciones se tienen que probar, por lo cual "haremos comparecer a los peritos de las partes y confrontar los documentos", como se hace en cualquier juzgado, aunque en este caso las conclusiones a las que llegue la ALDF no sean de carácter vinculatorio."A través de estas comparecencias tendremos muy claro las cosas que se hicieron, las que no se hicieron y las responsabilidades", afirmó.Jorge Gaviño explicó que a partir de ahí se reunirán los integrantes de la Comisión Especial que investiga las fallas de la Línea 12 del Metro, con el propósito de definir la o las fechas y el método de confrontación técnica entre peritos.Aclaró que las empresas están en su derecho de no participar en dicho debate, pero al final, las conclusiones a las que se llegue en el órgano legislativo tendrán un peso mayor, el de siete partidos políticos, que implicarán una "obligación moral, ética" de asumir las recomendaciones.Aseguró que en la comisión especial referida, integrada por 15 diputados de todos los partidos políticos representados en la ALDF, el interés común es que "esto no quede en la impunidad, que se ventile y se sepa lo que ocurrió".Gaviño explicó que al final de todo este proceso, los legisladores locales entregarán un informe, en el que se establecerán desde antecedentes hasta recomendaciones.Se presentarán un proyecto de informe al pleno, dijo, el cual será debatido, y una vez que se apruebe, se entregarán recomendaciones a autoridades locales, como el jefe de Gobierno, al propio Metro, al Proyecto Metro, al secretario de Obras, la Contraloría, para que finque responsabilidades.De igual manera, se pretenden reuniones con autoridades federales, como la Secretaría de la Función Pública y hasta la Auditoría Superior de la Federación.Gaviño informó también que fue invitado como testigo, como acompañante, mañana al encuentro que en la Cámara de Diputados tendrá el director general del STC Metro, Joel Ortega.\n', '', 'Home', 'g');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `milenio_articles_nd1`
--
ALTER TABLE `milenio_articles_nd1`
 ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `milenio_articles_nd1`
--
ALTER TABLE `milenio_articles_nd1`
MODIFY `id` int(8) NOT NULL AUTO_INCREMENT,AUTO_INCREMENT=40073;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
