import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Container, Row, Col, Button, Image, Alert, Spinner, Card, Badge, Form } from 'react-bootstrap';
import { useParams, useNavigate } from 'react-router-dom';
import { FaStar, FaRegStar, FaStarHalfAlt } from 'react-icons/fa';

interface Product {
  id: number;
  name: string;
  description: string;
  price: number;
  image_url: string;
  category_id: number;
  category_name: string;
  stock_quantity: number;
  average_rating: number;
  rating_count: number;
}

interface Review {
  id: number;
  user_name: string;
  rating: number;
  comment: string;
  created_at: string;
}

const ProductDetail: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const [product, setProduct] = useState<Product | null>(null);
  const [reviews, setReviews] = useState<Review[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const [quantity, setQuantity] = useState<number>(1);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchProductDetails = async () => {
      try {
        setLoading(true);
        const productResponse = await axios.get(`http://localhost:8002/api/v1/produkte/${id}`);
        setProduct(productResponse.data);
        
        // Reviews laden
        try {
          const reviewsResponse = await axios.get(`http://localhost:8002/api/v1/produkte/${id}/reviews`);
          setReviews(reviewsResponse.data);
        } catch (err) {
          console.error('Fehler beim Laden der Bewertungen:', err);
          // Wir setzen keinen Fehler, da Reviews optional sind
        }
        
        setLoading(false);
      } catch (err) {
        setError('Fehler beim Laden der Produktdetails');
        setLoading(false);
        console.error('Fehler beim Laden der Produktdetails:', err);
      }
    };

    if (id) {
      fetchProductDetails();
    }
  }, [id]);

  const handleQuantityChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const value = parseInt(e.target.value);
    if (value > 0 && product && value <= product.stock_quantity) {
      setQuantity(value);
    }
  };

  const addToCart = async () => {
    if (!product) return;
    
    try {
      await axios.post('http://localhost:8002/api/v1/warenkorb/add', {
        product_id: product.id,
        quantity: quantity
      });
      navigate('/cart');
    } catch (err) {
      console.error('Fehler beim Hinzufügen zum Warenkorb:', err);
    }
  };

  const renderStarRating = (rating: number) => {
    const stars = [];
    const fullStars = Math.floor(rating);
    const hasHalfStar = rating % 1 >= 0.5;
    
    for (let i = 1; i <= 5; i++) {
      if (i <= fullStars) {
        stars.push(<FaStar key={i} className="text-warning" />);
      } else if (i === fullStars + 1 && hasHalfStar) {
        stars.push(<FaStarHalfAlt key={i} className="text-warning" />);
      } else {
        stars.push(<FaRegStar key={i} className="text-warning" />);
      }
    }
    
    return (
      <div className="d-flex align-items-center">
        {stars}
        <span className="ms-2">({rating.toFixed(1)})</span>
      </div>
    );
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

  if (error || !product) {
    return <Alert variant="danger">{error || 'Produkt nicht gefunden'}</Alert>;
  }

  return (
    <Container className="my-5">
      <Row>
        <Col md={6}>
          {product.image_url ? (
            <Image 
              src={product.image_url} 
              alt={product.name} 
              fluid 
              className="product-detail-image"
            />
          ) : (
            <div className="bg-light text-center p-5">
              <span className="text-muted">Kein Bild verfügbar</span>
            </div>
          )}
        </Col>
        
        <Col md={6}>
          <h2>{product.name}</h2>
          
          <div className="mb-3">
            {renderStarRating(product.average_rating)}
            <span className="ms-2 text-muted">
              {product.rating_count} {product.rating_count === 1 ? 'Bewertung' : 'Bewertungen'}
            </span>
          </div>
          
          <h3 className="text-primary mb-3">{product.price.toFixed(2)} €</h3>
          
          <p>{product.description}</p>
          
          <div className="mb-3">
            <Badge bg="secondary">{product.category_name}</Badge>
            <Badge 
              bg={product.stock_quantity > 0 ? 'success' : 'danger'}
              className="ms-2"
            >
              {product.stock_quantity > 0 ? 'Auf Lager' : 'Nicht verfügbar'}
            </Badge>
            {product.stock_quantity > 0 && (
              <span className="ms-2 text-muted">
                {product.stock_quantity} verfügbar
              </span>
            )}
          </div>
          
          {product.stock_quantity > 0 && (
            <div className="d-flex align-items-center mb-4">
              <Form.Group className="me-3" style={{ width: '100px' }}>
                <Form.Label>Menge</Form.Label>
                <Form.Control 
                  type="number" 
                  value={quantity}
                  onChange={handleQuantityChange}
                  min="1"
                  max={product.stock_quantity}
                />
              </Form.Group>
              
              <Button 
                variant="primary" 
                onClick={addToCart}
                className="mt-auto"
              >
                In den Warenkorb
              </Button>
            </div>
          )}
        </Col>
      </Row>
      
      <hr className="my-5" />
      
      <h3 className="mb-4">Kundenbewertungen</h3>
      
      {reviews.length === 0 ? (
        <Alert variant="info">
          Dieses Produkt hat noch keine Bewertungen.
        </Alert>
      ) : (
        <Row>
          {reviews.map(review => (
            <Col md={6} key={review.id} className="mb-4">
              <Card>
                <Card.Body>
                  <div className="d-flex justify-content-between mb-2">
                    <strong>{review.user_name}</strong>
                    <small className="text-muted">
                      {new Date(review.created_at).toLocaleDateString()}
                    </small>
                  </div>
                  
                  <div className="mb-2">
                    {renderStarRating(review.rating)}
                  </div>
                  
                  <Card.Text>{review.comment}</Card.Text>
                </Card.Body>
              </Card>
            </Col>
          ))}
        </Row>
      )}
      
      <div className="d-flex justify-content-between mt-4">
        <Button variant="outline-secondary" onClick={() => navigate('/products')}>
          Zurück zu allen Produkten
        </Button>
      </div>
    </Container>
  );
};

export default ProductDetail; 