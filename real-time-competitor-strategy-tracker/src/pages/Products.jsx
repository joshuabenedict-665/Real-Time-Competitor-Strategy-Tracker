import ProductCard from "../components/ProductCard";

const dummyProducts = [
  { id: 1, name: "Sneakers", price: 2500, image: "/sneakers.jpg" },
  { id: 2, name: "Headphones", price: 4999, image: "/headphones.jpg" },
  { id: 3, name: "Smartwatch", price: 6999, image: "/smartwatch.jpg" },
];

export default function Products() {
  return (
    <div className="grid grid-cols-2 md:grid-cols-3 gap-6 p-8">
      {dummyProducts.map((product) => (
        <ProductCard key={product.id} product={product} />
      ))}
    </div>
  );
}
