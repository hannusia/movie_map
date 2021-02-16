import generate_map


def main():
    year = int(input('Please enter a year you would like to have a map for:'))
    location = list(map(float, input(
        'Please enter your location (format: lat, long): ').split(',')))
    print('map is generating...')
    print('please wait...')
    films = generate_map.read_file('locations(1).list', year)
    print(films[:10])
    filter = generate_map.filter_by_location(location[0], location[1], films)
    # print(filter)
    generate_map.generate_map(location[0], location[1], filter)
    print('Your map is generated. Look at the movies_map.html file.')


if __name__ == "__main__":
    main()
