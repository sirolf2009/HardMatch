namespace java com.hardmatch.matcher.thrift

struct Store {
1: string product
2: string store
3: double price
4: string url
5: string category
6: string stock
7: string img
}

service MatcherPHPHandler {

  /**
   * Match the specified components to the cheapest store
   * @param components - a list of components to be matched
   * @return a map with components name as key and the according store as value
   */
   map<string, Store> match(1: list<string> components)

}