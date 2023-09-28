ARG DOCKER_TAG=latest
FROM quay.io/keycloak/keycloak:${DOCKER_TAG} as builder

ARG THEME_JAR=keywind

# Enable health and metrics support
ENV KC_HEALTH_ENABLED=true
ENV KC_METRICS_ENABLED=true
ENV KC_HEALTH_ENABLED=true
ENV KC_HTTP_RELATIVE_PATH=/auth
ENV KC_FEATURES=preview,docker,fips

WORKDIR /opt/keycloak
# for demonstration purposes only, please make sure to use proper certificates in production instead
RUN keytool -genkeypair -storepass password -storetype PKCS12 -keyalg RSA -keysize 2048 -dname "CN=server" -alias server -ext "SAN:c=DNS:localhost,IP:127.0.0.1" -keystore conf/server.keystore
RUN /opt/keycloak/bin/kc.sh build

COPY ./${THEME_JAR}.jar /opt/keycloak/providers/${THEME_JAR}.jar

FROM quay.io/keycloak/keycloak:${DOCKER_TAG}
COPY --from=builder /opt/keycloak/ /opt/keycloak/

ENV TZ=Asia/Bangkok

ENTRYPOINT ["/opt/keycloak/bin/kc.sh"]