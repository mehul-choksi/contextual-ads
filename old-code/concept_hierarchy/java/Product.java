public class Product{

	String name;
	double price;
	HashMap<String, String> attributes;

	public Product(){
		attributes = new HashMap<>();
	}

	public Product(String name, double price, HashMap<String, String> attributes){
		this.name = name;
		this.price = price;
		this.attributes = attributes;
	}

	public void addAttribute(String key, String value){
		if(attributes.get(key) != null){
			System.out.println("Error, a value has already been allocated to the given field");
			return;
		}
		attributes.put(key,value);
	}

}
