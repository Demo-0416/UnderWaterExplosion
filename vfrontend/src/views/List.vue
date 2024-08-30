<<template>
  <div class="bg" >
      <div class="cube1">
      <h1>UnderWater Explosion</h1>
      </div>
      <div class="cube2">

      </div>
     
  </div>
</template>

<script setup>
import { Text } from 'vue';


</script>

<style scoped>
.bg {
  background-color: rgb(229, 229, 229);
  height: 100%;
  width: 100%;
  position: absolute;
}
.cube1 {
  width: 20%;
  height: 73.5% ;
  background-color: rgb(149, 145, 144);
  position: absolute;
  top: 10%;
  left: 2%;
  opacity: 0.35;
  
 
  box-shadow:3px 0 8px -4px rgba(75,75,75,0.4);
 
 /* background-image: url('@/assets/star.jpg'); /* 星空背景图 */
  background-size:cover;

}
.cube2 {
  width: 74.5%;
  height: 73.5% ;
  background-color: white;
  position: absolute;
  top: 10%;
  left: 24%;

 /* border-radius: 8px;*/
  box-shadow: 3px 0 8px -4px rgb(75, 75, 75);

}
/*.cube3 {
  width: 25%;
  height: 60% ;
  background-color: white;
  position: absolute;
  top: 10%;
  left: 76%;

}*/

</style>