import NavigationBar from './navigationBar'; 
import NavItem from './navItem';

const Layout = ({ children }: { children: React.ReactNode }) => {
  return (
    <>
      <NavigationBar>
        {/* Add the 'to' prop to each NavItem */}
        <NavItem text="Bayesian Methods" to="/bayesian" />
        <NavItem text="Statistical Methods" to="/statistical" />
        <NavItem text="Reliability Views" to="/reliability-views" />
      </NavigationBar>
      {children}
    </>
  );
};

export default Layout;