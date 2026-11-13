import streamlit as st

class TourPackage:
    def __init__(self, code, name, price, days, seats=14):
        self.code = code
        self.name = name
        self.price = price
        self.days = days
        self.seats = seats
        self.booked_seats = 0
        self.revenue = 0

class TravelSystem:
    def __init__(self):
        self.packages = [
            TourPackage("1", "Murchison Falls", 850000, 3),
            TourPackage("2", "Bwindi Gorilla Trekking", 2500000, 4),
            TourPackage("3", "Queen Elizabeth National Park", 900000, 3),
            TourPackage("4", "Ssese Islands", 450000, 2)
        ]
        self.bookings = []

    def calculate_cost(self, package, adults, children, accommodation):
        if package.code == "2" and children > 0:
            st.error("Gorilla trekking is only for persons aged 15 and above.")
            return None

        adult_price = package.price
        child_price = adult_price * 0.5 if children > 0 else 0

        if accommodation == 1:  
            extra = 0
        elif accommodation == 2:  
            extra = 150000 * (adults + children)
        else:  
            extra = 400000 * (adults + children)

        total = (adult_price * adults) + (child_price * children) + extra
        if (adults + children) >= 5:
            total *= 0.9  # 10% discount
        return total

    def book_tour(self, package, lead_name, adults, children, discount = 0):
        if (adults + children) >= 5:
            discount = 0.1
        total *= (1 - discount)
        return total, discount

    def book_tour(self, package, lead_name, adults, children, east_african, accommodation):
        if not east_african and package.seats < (adults + children):
            st.warning(f"Only {package.seats} seats left on this tour.")
            return None

        result = self.calculate_cost(package, adults, children, accommodation)
        if result is None:
            return None

        total_cost, discount = result
        deposit = 0.4 * total_cost
        balance = total_cost - deposit

        package.booked_seats += (adults + children)
        package.revenue += total_cost

        booking_ref = f"TRV-{len(self.bookings)+1:03d}"
        self.bookings.append({
            "ref": booking_ref,
            "package": package.name,
            "travellers": adults + children,
            "accommodation": accommodation,
            "discount": discount,
            "total": total_cost,
            "deposit": deposit,
            "balance": balance
        })
        return booking_ref, total_cost, deposit, balance

def main():
    st.title("Tours & Travel System")
    system = TravelSystem()

    menu = st.sidebar.selectbox("Menu", ["Book a Tour", "View Summary", "About"])

    if menu == "Book a Tour":
        st.subheader("Available Tour Packages")
        package_code = st.selectbox("Choose Package", 
            [f"{p.code}: {p.name} ({p.days} days) - UGX {p.price}" for p in system.packages])
        package = next((p for p in system.packages if p.code == package_code.split(":")[0]), None)

        lead_name = st.text_input("Lead Traveller Name")
        adults = st.number_input("Number of Adults", min_value=1, value=1)
        children = st.number_input("Number of Children", min_value=0, value=0)
        east_african = st.checkbox("East African Citizens")
        accommodation = st.selectbox("Accommodation", ["Budget", "Mid-range", "Luxury"])
        acc_value = 1 if accommodation=="Budget" else 2 if accommodation=="Mid-range" else 3

        if st.button("Book Tour"):
            result = system.book_tour(package, lead_name, adults, children, east_african, acc_value)
            if result:
                ref, total, dep, bal = result
                st.success("Booking Confirmed!")
                st.write(f"Reference: {ref}")
                st.write(f"Package: {package.name}")
                st.write(f"Travellers: {adults + children}")
                st.write(f"Accommodation: {accommodation}")
                st.write(f"Total Cost: UGX {total:.2f}")
                st.write(f"Deposit (40%): UGX {dep:.2f}")
                st.write(f"Balance: UGX {bal:.2f}")

    elif menu == "View Summary":
        st.subheader("Bookings Summary")
        for pkg in system.packages:
            st.write(f"{pkg.name}: Seats booked = {pkg.booked_seats}, Revenue = UGX {pkg.revenue:.2f}")

    else:
        st.write("About this Tours & Travel System...")
        st.write("Built By SHADIRNET for Uganda tourism bookings.")

if __name__ == "__main__":
    main()
