import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Card, Button, Container, Row, Col, Spinner } from 'react-bootstrap';

interface Product {
  id: number;
  name: string;
  description: string;
  price: number;
  image_url: string;
  category_id: number;
  stock_quantity: number;
}

const ProductList: React.FC = () => {
  const [products, setProducts] = useState<Product[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchProducts = async () => {
      try {
        setLoading(true);
        const response = await axios.get('http://localhost:8002/api/v1/produkte');
        setProducts(response.data);
        setLoading(false);
      } catch (err) {
        setError('Fehler beim Laden der Produkte');
        setLoading(false);
        console.error('Fehler beim Laden der Produkte:', err);
      }
    };

    fetchProducts();
  }, []);

  const addToCart = async (productId: number) => {
    try {
      await axios.post('http://localhost:8002/api/v1/warenkorb/add', { product_id: productId, quantity: 1 });
      // Benachrichtigung oder Feedback hier einfügen
    } catch (err) {
      console.error('Fehler beim Hinzufügen zum Warenkorb:', err);
    }
  };

  if (loading) {
    return (
      <div className="text-center my-5">
        <Spinner animation="border" role="status">
          <span className="visually-hidden">Lädt...</span>
        </Spinner>
      </div>
    );
  }

  if (error) {
    return <div className="alert alert-danger">{error}</div>;
  }

  return (
    <Container>
      <h2 className="my-4">Produkte</h2>
      <Row>
        {products.map((product) => (
          <Col key={product.id} md={4} className="mb-4">
            <Card>
              {product.image_url && (
                <Card.Img 
                  variant="top" 
                  src={product.image_url} 
                  alt={product.name}
                  style={{ height: '200px', objectFit: 'cover' }}
                />
              )}
              <Card.Body>
                <Card.Title>{product.name}</Card.Title>
                <Card.Text>{product.description}</Card.Text>
                <Card.Text className="fw-bold">{product.price.toFixed(2)} €</Card.Text>
                <Button 
                  variant="primary" 
                  onClick={() => addToCart(product.id)}
                  disabled={product.stock_quantity <= 0}
                >
                  {product.stock_quantity > 0 ? 'In den Warenkorb' : 'Nicht verfügbar'}
                </Button>
              </Card.Body>
            </Card>
          </Col>
        ))}
      </Row>
    </Container>
  );
};

export default ProductList; 