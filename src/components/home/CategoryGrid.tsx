import Link from 'next/link'
import { FileText, Printer, Computer, Armchair, Scissors, Package } from 'lucide-react'

export default function CategoryGrid() {
  const categories = [
    { name: 'Office Supplies', icon: Scissors, color: 'bg-blue-100 text-blue-600' },
    { name: 'Paper Products', icon: FileText, color: 'bg-green-100 text-green-600' },
    { name: 'Ink & Toner', icon: Printer, color: 'bg-purple-100 text-purple-600' },
    { name: 'Technology', icon: Computer, color: 'bg-red-100 text-red-600' },
    { name: 'Furniture', icon: Armchair, color: 'bg-amber-100 text-amber-600' },
    { name: 'Storage', icon: Package, color: 'bg-teal-100 text-teal-600' },
  ]

  return (
    <section className="container mx-auto px-4 py-16">
      <h2 className="text-3xl font-bold text-center mb-12">Shop by Category</h2>
      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-6">
        {categories.map((category) => (
          <Link
            key={category.name}
            href={`/products?category=${category.name.toLowerCase().replace(' ', '-')}`}
            className="group"
          >
            <div className="bg-white p-6 rounded-lg shadow-md hover:shadow-xl transition text-center">
              <div className={`${category.color} w-16 h-16 rounded-full mx-auto mb-4 flex items-center justify-center group-hover:scale-110 transition`}>
                <category.icon size={32} />
              </div>
              <h3 className="font-semibold text-gray-800">{category.name}</h3>
            </div>
          </Link>
        ))}
      </div>
    </section>
  )
}