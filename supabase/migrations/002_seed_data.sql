-- Restaurant Voice Agent - Seed Data
-- Sample menu for testing

INSERT INTO menu_items (name, description, price, category, allergens) VALUES
-- Entrées
('Soupe à l''oignon gratinée', 'Soupe traditionnelle avec croûtons et fromage gratiné', 8.50, 'entrées', ARRAY['gluten', 'lactose']),
('Escargots de Bourgogne', '6 escargots au beurre persillé', 12.00, 'entrées', ARRAY['lactose']),
('Foie gras maison', 'Servi avec chutney de figues et toast', 18.00, 'entrées', ARRAY['gluten']),
('Salade Lyonnaise', 'Salade frisée, lardons, œuf poché, croûtons', 11.00, 'entrées', ARRAY['gluten', 'oeufs']),
('Terrine de campagne', 'Terrine traditionnelle, cornichons, pain grillé', 10.00, 'entrées', ARRAY['gluten']),

-- Plats
('Boeuf Bourguignon', 'Mijoté au vin rouge, carottes et champignons', 24.00, 'plats', ARRAY[]::TEXT[]),
('Confit de canard', 'Cuisse confite, pommes sarladaises', 22.00, 'plats', ARRAY[]::TEXT[]),
('Sole meunière', 'Sole entière, beurre citronné, pommes vapeur', 28.00, 'plats', ARRAY['lactose', 'poisson']),
('Steak frites', 'Entrecôte 300g, frites maison, sauce au poivre', 26.00, 'plats', ARRAY['lactose']),
('Coq au vin', 'Coq mijoté au vin rouge, champignons, lardons', 23.00, 'plats', ARRAY[]::TEXT[]),
('Blanquette de veau', 'Veau mijoté à la crème, riz pilaf', 22.00, 'plats', ARRAY['lactose']),
('Magret de canard', 'Magret rosé, sauce aux cerises, gratin dauphinois', 25.00, 'plats', ARRAY['lactose']),

-- Desserts
('Crème brûlée', 'À la vanille de Madagascar', 9.00, 'desserts', ARRAY['lactose', 'oeufs']),
('Tarte Tatin', 'Tarte aux pommes caramélisées, crème fraîche', 10.00, 'desserts', ARRAY['gluten', 'lactose']),
('Fondant au chocolat', 'Coeur coulant, glace vanille', 11.00, 'desserts', ARRAY['gluten', 'lactose', 'oeufs']),
('Mousse au chocolat', 'Mousse légère au chocolat noir', 8.00, 'desserts', ARRAY['lactose', 'oeufs']),
('Profiteroles', 'Choux garnis de glace vanille, sauce chocolat', 10.00, 'desserts', ARRAY['gluten', 'lactose', 'oeufs']),
('Île flottante', 'Meringue pochée, crème anglaise, caramel', 9.00, 'desserts', ARRAY['lactose', 'oeufs']);
